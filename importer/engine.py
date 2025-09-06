from manager import * 
import pandas as pd
import os
import pymongo
import logging
import sys

PROD_DBNAME = "prod_dbname"
DBNAME = "dbname"
USERNAME = "username" 
PASSWORD  = "password" 
HOST = "host"
PORT = "port" 
DEBUG_MODE = "debug_mode"
START = "start" 
LIMIT = "limit"
TRACE_ONLY = "trace_only"
CLEAN_DB = "clean_db"
DOCKMODE = "dockmode"
DOCNAME  = "docname"


CFG= {}
STARS = "*" * 50
BLANK = ""

def handle_critical(message):
    logging.critical(message)
    logging.critical(f"Abnormal end of execution")
    sys.exit(1)

class Engine():
    """
    Importer Engine for processing and migrating healthcare data.
    """

    def __init__(self,config):
        """
        Initialize the Engine with logging and configuration.
        """ 
        global CFG
        CFG = config
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info(STARS)
        self.log.info("Importer Engine starts ")
        self.df = None
        self.db = None
        self.fm = FieldManager()


    def load_df(self, df):
        """
        Load a DataFrame or CSV file into the engine.
        """
        try :
            if isinstance(df,pd.DataFrame):
                self.log.info(f"DataFrame loaded")
            elif os.path.exists(df) and (df[-4:]).lower() == ".csv":
                df = pd.read_csv(df,dtype=str)
            else:
               self.log.error("DF loader : Error with your entry, must be a dataframe or a csv file" )
        except Exception as e:
            self.log.error("DF loader : Error with your entry, must be a dataframe or a csv file" )
            exit()
        if CFG[START] or CFG[LIMIT]:
            df = df.iloc[CFG[START]:CFG[START]+CFG[LIMIT]]
        self.df = df
        self.log.info(BLANK)
        return self.df

    def clean_df(self):
        """
        Clean the DataFrame by converting and validating fields.
        """
        self.log.info("Clean data before migration...")

        for fieldname in self.fm.fields :
            if fieldname != PK_ID:
                self.fm.convert_df_values(self.df,fieldname)      
                self.fm.apply_mask(self.df,fieldname)
        self.log.info(BLANK)
        return self.df

    def make_unic_df(self):
        """
        Make the DataFrame unique by removing duplicates.
        """
        subset=self.fm.get_pk_fields()
        mask = self.df.duplicated(subset=subset, keep="last")
        duplicated = self.df[mask].sort_values("Name")
        to_delete = len(duplicated)
        if to_delete:
            logging.warning("Duplicates detected. Only latest is retained, suppressing following elements.")
            logging.warning(duplicated.to_string())
            self.df.drop(duplicated.index, inplace=True)
        else:
            logging.info("No duplicate detected in the dataset.")
        self.log.info(BLANK)
        return self.df


    def upsert_rows(self):
        count_inserted = 0
        total = len(self.df)
        self.log.info(STARS)
        self.log.info(f"Migration start with {total} documents fter cleaning and merging.")
        for i, row in self.df.iterrows():
            self.upsert_row(row.to_dict())
            count_inserted += 1
        self.log.info(f"Migration complete: {count_inserted} documents inserted out of {total} rows processed.")
        self.log.info(BLANK)



    def upsert_row(self, row : dict):
        """
        Upsert a dataframe row into the MongoDB collection.
        """
        doc , pk = self.fm.get_doc(row)
        self.log.debug(f"Document constructed: {doc}")
        if not CFG[TRACE_ONLY]:
            try:
                result = self.db.care.replace_one({PK_ID: doc[PK_ID]}, doc, upsert=True)
                operation = "inserted" if result.upserted_id else "updated"
                self.log.info(f"Document {doc[PK_ID]} {operation}: {pk}")
            except Exception as e:
                self.log.warning(f"Error inserting row {e}  /n{pk}")
        else:
            self.log.info("Document non upserted - Trace Only mode")
            

    def initialize_db(self):
        """
        Initialize the database collections, schema, and indexes.
        """
        self.log.info("Try to initialize MongoDB.")

        if not CFG[TRACE_ONLY] :
            self.log.info("Db initialization non performed - Trace Only mode")
            return
        self.log.info("Db initialization started")
        dbname = CFG[DBNAME]                
        # Clean DB, security, schema and index
        if CFG[CLEAN_DB]:
            self.log.warning(f"Collection {dbname}, schema and index deletion.")
            self.db.drop_collection(CFG[DOCNAME])
            self.log.warning(f"All roles of Mongodb deletion.")
            self.db.command("dropAllRolesFromDatabase")

        
        
        # exit function if not first run
        if CFG[DOCNAME] in self.db.list_collection_names():
            self.log.info(f"Collection {CFG[DOCNAME]} already exists, no modification applied.")
            return

        try:
            schema = self.fm.build_mongodb_schema()
            self.db.create_collection(CFG[DOCNAME], validator=schema)
            self.log.info(f"Collection {CFG[DOCNAME]} created with JSON Schema validation.")
        except pymongo.errors.CollectionInvalid as e:
            self.log.warning(f"Error creating collection: {e}")
            return
        
        collection = self.db[CFG[DOCNAME]]

        for index in self.fm.get_indexes():
            try:
                collection.create_index(index)
                self.log.info(f"Index {index} created.")
            except pymongo.errors.OperationFailure as e:
                self.log.warning(f"Failed to create index {index}.", e)

        replace_dict= {"${dbname}": dbname}
        data = load_yaml("data/mongodb_roles.yml", replace=replace_dict)
        roles = data['roles']

        for role in roles:
            try:
                self.db.command(role)
                self.log.info(f"Role {role['createRole']} created.")
            except pymongo.errors.OperationFailure as e:
                self.log.warning(f"Error during role {role['createRole']} creation :", e)



    def connect_db(self):
        """
        Get the MongoDB database connection.
        """
        # MongoDB connection via pymongo
        self.log.info("Try to connect to MongoDB.")
        try:
            cnxstr = f"mongodb://{CFG[USERNAME]}:{CFG[PASSWORD]}@{CFG[HOST]}:{CFG[PORT]}/"
            client = pymongo.MongoClient(cnxstr)
            # check if mongodb prod server
            self.db = client[CFG[PROD_DBNAME]]
            coll_names = self.db.list_collection_names()
            if not CFG[DOCKMODE] and CFG[DOCNAME] in coll_names:
                handle_critical(f"Connected to Production MongoDB server not allowed")
                return

            self.db = client[CFG[DBNAME]]
            self.log.info("Connection established.")
            self.log.info(BLANK)
        except pymongo.errors.OperationFailure as e:
            handle_critical(f"No connection : review your .env settings", e)
    
    
    def import_df(self):
        """
        Extract, transform and load a DataFrame into MongoDB.
        """
        # Main function for migrating DataFrame to MongoDB
        self.log.info(f"Execution options - start: {CFG[START]}, limit: {CFG[LIMIT]}, TRACE_ONLY: {CFG[TRACE_ONLY]}")

        self.connect_db()
        self.initialize_db()

        self.clean_df()

        self.log.info("Remove  duplicates...")
        self.df = self.make_unic_df()

        self.upsert_rows()

        self.log.info(BLANK)


