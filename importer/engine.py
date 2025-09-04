from manager import * 
import pandas as pd
import os
import pymongo
import json
import logging

DBNAME = "dbname"
USERNAME = "username" 
PASSWORD  = "password" 
HOST = "host"
PORT = "port" 
DEBUG_MODE = "debug_mode"
START = "start" 
LIMIT = "limit"
TRACEONLY = "traceonly"
CLEANDB = "cleandb"



class Engine():

    
    def __init__(self, settings:dict):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info("="*50)
        self.log.info("Importer Engine starts ")
        self.df = None
        self.db = None
        self.settings = settings
        self.fm = FieldManager()


    def load_df(self, df):
        try :
            if isinstance(df,pd.DataFrame):
                self.log.info(f"DataFrame loaded")
            elif os.path.exists(df) and (df[-4:]).lower() == ".csv":
                df = pd.read_csv(df,dtype=str)
            else:
               self.log.error("DF loader : Error with your entry, must be a dataframe or a csv file" )
        except Exception as e:
            self.log.error("DF loader : Error with your entry, must be a dataframe or a csv file" )
        if self.settings[START] or self.settings[LIMIT]:
            df = df.iloc[self.settings[START]:self.settings[START]+self.settings[LIMIT]]
        self.df = df
        return self.df

    def clean_df(self):
        
        for fieldname in self.fm.fields :
            if fieldname != PK_ID:
                self.fm.convert_df_values(self.df,fieldname)      
                self.fm.apply_mask(self.df,fieldname)
        return self.df

    def make_unic_df(self):
        # Handles duplicates by keeping only the latest
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
        # Transforms a CSV row into a MongoDB document and inserts or updates
        doc , pk = self.fm.get_doc(row)
        self.log.debug(f"Document constructed: {doc}")
        if not self.settings[TRACEONLY]:
            try:
                result = self.db.care.replace_one({PK_ID: doc[PK_ID]}, doc, upsert=True)
                operation = "inserted" if result.upserted_id else "updated"
                self.log.info(f"Document {doc[PK_ID]} {operation}: {pk}")
            except Exception as e:
                self.log.error(f"Error inserting row {e}  /n{pk}")
        else:
            self.log.info("Document non upserted - Trace Only mode")
            

    def initialize_db(self):
        # Collection initialization and index creation
        dbname = self.settings[DBNAME]
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
        if self.settings[CLEANDB]:
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
            self.log.error(f"Error creating collection: {e}")
            return
        
        collection = self.db[DOCNAME]

        for index in self.fm.get_indexes():
            try:
                collection.create_index(index)
                self.log.info(f"Index {index} created.")
            except pymongo.errors.OperationFailure as e:
                self.log.error(f"Failed to create index {index}.", e)

        for role in roles:
            try:
                self.db.command(role)
                self.log.info(f"Role {role['createRole']} created.")
            except pymongo.errors.OperationFailure as e:
                self.log.error(f"Error during role {role['createRole']} creation :", e)



    def get_db(self):
        # MongoDB connection via pymongo
        cnxstr = f"mongodb://{self.settings[USERNAME]}:{self.settings[PASSWORD]}@{self.settings[HOST]}:{self.settings[PORT]}/"
        client = pymongo.MongoClient(cnxstr)
        self.db = client[self.settings[DBNAME]]
        if not self.settings[TRACEONLY] :
            self.initialize_db()
        else:
            self.log.info("Db initialization non performed - Trace Only mode")

    def import_df(self):
        # Main function for migrating DataFrame to MongoDB
        self.log.info(f"Execution options - start: {self.settings[START]}, limit: {self.settings[LIMIT]}, traceonly: {self.settings[TRACEONLY]}")
        self.log.info("Cleaning data before migration...")
        self.get_db()
        self.clean_df()
        self.log.info("Processing duplicates...")
        self.df = self.make_unic_df()
        count_inserted = 0
        total = len(self.df)
        self.log.info(f"Total rows after cleaning and merging: {total}")
        for i, row in self.df.iterrows():
            self.upsert_row(row.to_dict())
            count_inserted += 1
        self.log.info(f"Migration complete: {count_inserted} documents inserted out of {total} rows processed.")
