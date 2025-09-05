from manager import * 
import pandas as pd
import os
import pymongo
import json
import logging
import sys

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

CFG= {}
STARS = "="*50
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
        self.log.info("="*50)
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
        return self.df

    def clean_df(self):
        """
        Clean the DataFrame by converting and validating fields.
        """
        for fieldname in self.fm.fields :
            if fieldname != PK_ID:
                self.fm.convert_df_values(self.df,fieldname)      
                self.fm.apply_mask(self.df,fieldname)
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
        return self.df

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

        # Collection initialization and index creation
        dbname = CFG[DBNAME]
        roles = [
            {   "createRole": "healthcareOperator",
                "privileges": [
                    { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },
                    { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },
                    { "resource": {"db": f"{dbname}", "collection": "observation"}, "actions": ["find"] },
               ],
                "roles": []},
            {   "createRole": "healthcareManager",
                "privileges": [
                    { "resource": {"db": f"{dbname}", "collection": "observation"}, "actions": ["find", "insert", "update", "remove"] },
                    { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },            
                    { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },            
                ],
                "roles": []
            },
            {   "createRole": "administrativeOperator",
                "privileges": [
                    { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },
                    { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },
                    { "resource": {"db": f"{dbname}", "collection": "billing"}, "actions": ["find"] },
                ],
                "roles": []
            },
            {   "createRole": "administrativeManager",
                "privileges": [
                    { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find", "insert", "update", "remove"] },
                    { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find", "insert", "update", "remove"] },
                    { "resource": {"db": f"{dbname}", "collection": "billing"}, "actions": ["find", "insert", "update", "remove"] },
                ],
                "roles": []
            },
            {   "createRole": "accountingManager",
                "privileges": [
                    { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },
                    { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },
                    { "resource": {"db": f"{dbname}", "collection": "billing"}, "actions": ["find", "insert", "update", "remove"] },            
                ],
                "roles": []
            }
        ]

        # Clean DB, security, schema and index
        if CFG[CLEAN_DB]:
            self.log.warning(f"Collection {dbname}, schema and index deletion.")
            self.db.drop_collection(DOCNAME)
            self.db.command("dropAllRolesFromDatabase")
            self.log.warning(f"All roles of Mongodb deletion.")

        
        
        # exit function if not first run
        if DOCNAME in self.db.list_collection_names():
            self.log.info(f"Collection {DOCNAME} already exists, no modification applied.")
            return
        try:
            schema_filepath = "data/schema_validation.json"
            with open(schema_filepath, "r") as f:
                schema = json.load(f)
            self.db.create_collection(DOCNAME, validator=schema)
            self.log.info(f"Collection {DOCNAME} created with JSON Schema validation.")
        except pymongo.errors.CollectionInvalid as e:
            self.log.warning(f"Error creating collection: {e}")
            return
        
        collection = self.db[DOCNAME]

        for index in self.fm.get_indexes():
            try:
                collection.create_index(index)
                self.log.info(f"Index {index} created.")
            except pymongo.errors.OperationFailure as e:
                self.log.warning(f"Failed to create index {index}.", e)

        for role in roles:
            try:
                self.db.command(role)
                self.log.info(f"Role {role['createRole']} created.")
            except pymongo.errors.OperationFailure as e:
                self.log.warning(f"Error during role {role['createRole']} creation :", e)



    def get_db(self):
        """
        Get the MongoDB database connection.
        """
        # MongoDB connection via pymongo
        try:

            cnxstr = f"mongodb://{CFG[USERNAME]}:{CFG[PASSWORD]}@{CFG[HOST]}:{CFG[PORT]}/"
            client = pymongo.MongoClient(cnxstr)
            self.db = client[CFG[DBNAME]]
            self.log.info("Connection established.")
        except pymongo.errors.OperationFailure as e:
            handle_critical(f"No connection : review your .env settings", e)
    
    
    def import_df(self):
        """
        Extract, transform and load a DataFrame into MongoDB.
        """
        # Main function for migrating DataFrame to MongoDB
        self.log.info(f"Execution options - start: {CFG[START]}, limit: {CFG[LIMIT]}, TRACE_ONLY: {CFG[TRACE_ONLY]}")

        self.log.info("Try to connect to MongoDB.")
        self.get_db()
        self.log.info(BLANK)

        if not CFG[TRACE_ONLY] :
            self.log.info("Db initialization started")
            self.initialize_db()
            self.log.info(BLANK)
        else:
            self.log.info("Db initialization non performed - Trace Only mode")

        self.log.info("Cleaning data before migration...")
        self.clean_df()
        self.log.info(BLANK)

        self.log.info("Removing  duplicates...")
        self.df = self.make_unic_df()
        self.log.info(BLANK)

        count_inserted = 0
        total = len(self.df)
        self.log.info(f"Total rows after cleaning and merging: {total}")
        for i, row in self.df.iterrows():
            self.upsert_row(row.to_dict())
            count_inserted += 1
        self.log.info(f"Migration complete: {count_inserted} documents inserted out of {total} rows processed.")
        self.log.info(BLANK)


