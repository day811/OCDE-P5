#importer/manager.py

from importer.manager import * 
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


    def load_df(self, source):
        """
        Load a DataFrame, Dictionary or CSV file into the engine.
        """
        df = pd.DataFrame()
        try :
            if isinstance(source,pd.DataFrame) or isinstance(source,dict):
                df = pd.DataFrame(source,dtype=str)                
                self.log.info(f"Dictionnary loaded")
            elif os.path.exists(source) and (source[-4:]).lower() == ".csv":
                df = pd.read_csv(source,dtype=str)
                self.log.info(f"CSV {source} loaded")
            else:
               self.log.error("DF loader : Error with your entry, must be a dataframe, a dictionnary or a csv file" )
        except Exception as e:
            handle_critical("DF loader : Error with your entry, must be a dataframe, a dictionnary or a csv file" )
        
        
        for fieldname in self.fm.fields.keys():
            if fieldname not in df.columns and not fieldname.startswith("_id"):
                self.log.critical("DF loader : Error with your entry, field {fieldname} not in the dataframe" )
                return pd.DataFrame()
                
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
            if not fieldname.startswith(PK_ID):
                self.fm.convert_df_values(self.df,fieldname)      
                self.fm.apply_mask(self.df,fieldname)
        self.log.info(BLANK)
        return self.df

    def make_unic_df(self):
        """
        Make the DataFrame unique by removing duplicates.
        """
        subset=self.fm.get_pk_fields('care')
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
        """
        Iterate dataframe rows to upsert
        """
        count_inserted = 0
        total = len(self.df)
        self.log.info(STARS)
        self.log.info(f"Migration start with {total} documents after cleaning and merging.")
        for i, row in self.df.iterrows():
            self.upsert_row(row.to_dict())
            count_inserted += 1
        self.log.info(f"Migration complete: {count_inserted} documents inserted out of {total} rows processed.")
        self.log.info(BLANK)


    def upsert_row(self, row : dict):
        """
        Upsert a dataframe row into the MongoDB collection.
        """
        jsondoc , pk = self.fm.get_doc(row)
        
        for document_name, document in jsondoc.items():

            self.log.debug(f"Document constructed: {document}")
            if not CFG[TRACE_ONLY]:
                try:
                    result = self.db[document_name].replace_one({PK_ID: document[PK_ID]}, document, upsert=True)
                    operation = "inserted" if result.upserted_id else "updated"
                    self.log.info(f"{document_name} collection : {document[PK_ID]} {operation}: {pk}")
                except Exception as e:
                    self.log.warning(f"Error inserting row {e}  /n{pk}")
            else:
                self.log.info("Document non upserted - Trace Only mode")
        return jsondoc
                

    def initialize_db(self):
        """
        Initialize the database collections, schema, indexes and roles.
        """
        self.log.info("Try to initialize MongoDB.")

        if CFG[TRACE_ONLY] :
            self.log.info("Db initialization non performed - Trace Only mode")
            return
        self.log.info("Db initialization started")

        json_schema = self.fm.build_mongodb_schema()
        dbname = CFG[DBNAME]                

        # browse through master collections to delete
        for docname, schema_doc in json_schema.items():

            # Clean DB, security, schema and index , only in test mode
            if CFG[CLEAN_DB]:
                self.log.warning(f"Collection '{docname}': data, schema and index deletion.")
                self.db.drop_collection(docname)
       
            # exit function if collection already exists in db
            if docname in self.db.list_collection_names():
                self.log.info(f"Collection {docname} already exists, no modification applied.")
                return

        
            try:
                self.log.debug(f"Collection {docname} JSON Schema validation : ")
                self.log.debug(schema_doc)
                self.db.create_collection(docname, validator=schema_doc)
                self.log.info(f"Collection {docname} created with JSON Schema validation.")
            except pymongo.errors.CollectionInvalid as e:
                self.log.warning(f"Error creating collection {docname} : {e}")
                return
            

            for index in self.fm.get_indexes(docname):
                try:
                    self.log.debug(f"Index de {docname}  : {index} ")
                    self.log.debug(schema_doc)
                    self.db[docname].create_index(index)
                    self.log.info(f"Index {index} created.")
                except pymongo.errors.OperationFailure as e:
                    self.log.warning(f"Failed to create index {index}.", e)

        
        if CFG[CLEAN_DB]:
            self.log.warning(f"All roles of Mongodb deletion.")
            self.db.command("dropAllRolesFromDatabase")
        replace_dict= {"${dbname}": dbname}
        data = load_yaml("data/mongodb_roles.yml", replace=replace_dict)
        roles = data['roles']

        for role in roles:
            try:
                self.log.debug(f"JSON role : {str(role)} ")
                self.db.command(role)
                self.log.info(f"Role {role['createRole']} created.")
            except pymongo.errors.OperationFailure as e:
                self.log.warning(f"Error during role {role['createRole']} creation :", e)
        return self.db


    def connect_db(self):
        """
        Get the MongoDB database connection.
        """
        self.log.info("Try to connect to MongoDB.")
        try:
            cnxstr = f"mongodb://{CFG[USERNAME]}:{CFG[PASSWORD]}@{CFG[HOST]}:{CFG[PORT]}/"
            client = pymongo.MongoClient(cnxstr)
            # check if mongodb prod server
            self.db = client[CFG[PROD_DBNAME]]
            coll_names = self.db.list_collection_names()
            first_collection = self.fm.get_masterdoc_list()[0]
            if not CFG[DOCKMODE] and first_collection in coll_names:
                handle_critical(f"Connected to Production MongoDB server not allowed")
                return

            self.db = client[CFG[DBNAME]]
            self.log.info("Connection established.")
            self.log.info(BLANK)
        except pymongo.errors.OperationFailure as e:
            handle_critical(f"No connection : review your .env settings", e)
        return self.db
    
    
    def import_df(self):
        """
        Transform and load the loaded DataFrame into MongoDB.
        """
        self.log.info(f"Execution options - start: {CFG[START]}, limit: {CFG[LIMIT]}, TRACE_ONLY: {CFG[TRACE_ONLY]}")

        self.connect_db()
        self.initialize_db()

        self.clean_df()

        self.log.info("Remove  duplicates...")
        self.df = self.make_unic_df()

        self.upsert_rows()

        self.log.info(BLANK)


