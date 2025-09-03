import pandas as pd
from decimal import Decimal
from datetime import datetime
import pymongo
import os
from dotenv import load_dotenv
import logging
import hashlib
import json

load_dotenv()

# Loads environment variables from .env
dockmode = os.getenv("DOCKMODE", "0")
dockmode = dockmode.lower() in ["true", "1", "yes"]
dbname = os.getenv("MONGO_DB_NAME", "test")
username = os.getenv("MONGO_INITDB_ROOT_USERNAME","admin")
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "secret")
host = os.getenv("MONGO_HOST", "mongo") 
port = int(os.getenv("MONGO_PORT", 27017))

debug_mode = os.getenv("MIGRATION_DEBUG", "0")
debug_mode = debug_mode.lower() in ["true", "1", "yes"]
debug_start = int(os.getenv("DEBUG_START", 0))
debug_limit = int(os.getenv("DEBUG_LIMIT", 0))
debug_traceonly = os.getenv("DEBUG_TRACE_ONLY", "1")
debug_traceonly = debug_traceonly.lower() in ["true", "1", "yes"]

# if needed overwrite settings in interactive/test mode 
if not dockmode:
    host = "localhost"
    debug_start = 0
    debug_limit = 10
    debug_traceonly = False


unic_subset = ["Name", "Gender", "Date of Admission", "Hospital", "Doctor", "Medical Condition"]
db_collection_name = "care"

# Logger configuration
loglvl = logging.INFO if not debug_mode else logging.DEBUG
logging.basicConfig(
    filename="logs/migration_healthcare.log", 
    level=loglvl, 
    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Logger configured")

documentmap = {
    "patient": ["Name", "Age", "Gender", "Blood Type"],
    "admission": ["Date of Admission", "Doctor", "Hospital", "Room Number", "Admission Type", "Discharge Date"],
    "billing": ["Insurance Provider", "Billing Amount"],
    "observation": ["Medical Condition", "Medication", "Test Results"],
}
administrative_collections = ["patient", "admission", "billing"]
healthcare_collections = ["patient","admission","observation"]
accounting_collections = "billing"

roles = [
    {   
        "createRole": "healthcareOperator",
        "privileges": [
            { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },
            { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },
            { "resource": {"db": f"{dbname}", "collection": "observation"}, "actions": ["find"] },
        ],
        "roles": []},
    {
        "createRole": "healthcareManager",
        "privileges": [
            { "resource": {"db": f"{dbname}", "collection": "observation"}, "actions": ["find", "insert", "update", "remove"] },
            { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },            
            { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },            
        ],
        "roles": []
    },
    {
        "createRole": "administrativeOperator",
        "privileges": [
            { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },
            { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },
            { "resource": {"db": f"{dbname}", "collection": "billing"}, "actions": ["find"] },
        ],
        "roles": []
    },
    {
        "createRole": "administrativeManager",
        "privileges": [
            { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find", "insert", "update", "remove"] },
            { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find", "insert", "update", "remove"] },
            { "resource": {"db": f"{dbname}", "collection": "billing"}, "actions": ["find", "insert", "update", "remove"] },
        ],
        "roles": []
    },
    {
        "createRole": "accountingManager",
        "privileges": [
            { "resource": {"db": f"{dbname}", "collection": "patient"}, "actions": ["find"] },
            { "resource": {"db": f"{dbname}", "collection": "admission"}, "actions": ["find"] },
            { "resource": {"db": f"{dbname}", "collection": "billing"}, "actions": ["find", "insert", "update", "remove"] },            
        ],
        "roles": []
    }
]

def process_mask(df, mask, column, replace=False):
    # Handles incorrect values by excluding or replacing depending on parameter
    rows_to_log = df[mask]
    if len(rows_to_log):
        logging.warning(f"Incorrect values detected in column {column}.")
        logging.warning(f"Concerned rows: {rows_to_log}")
        if replace is not False:
            df.loc[mask, column] = replace
            logging.info(f"Replacement of column {column} with {replace} for above rows.")
        else:
            df.drop(df[mask].index, inplace=True)
            logging.info(f"Excluding rows with incorrect values in {column}.")
    else:
        logging.info(f"No anomaly detected in column {column}.")

def convert_to_int(val, dft=None):
    try:
        return int(val)
    except (ValueError, TypeError) as e:
        logging.error(f"Error converting to int for value {val}: {e}")
        return dft

def convert_to_float(val, dft=None):
    try:
        return float(val)  # Compatible with MongoDB
    except (ValueError, TypeError) as e:
        logging.error(f"Error converting to float for value {val}: {e}")
        return dft

def convert_to_date(val, format="%Y-%m-%d", dft=None):
    try:
        if pd.isna(val):
            return dft
        return datetime.strptime(val, format)
    except (ValueError, TypeError) as e:
        logging.error(f"Error converting to date for value {val}: {e}")
        return dft

def clean_df(df):
    # Cleans and validates the DataFrame
    logging.info("Mapping CSV fields to MongoDB sub-documents...")
    col = "Name"
    mask = df[col].isna()
    process_mask(df, mask, col)
    logging.info("Processed Name...")

    col = "Age"
    df[col] = df[col].apply(convert_to_int)
    mask = (df[col] < 0) | (df[col] > 120) | df[col].isna()
    process_mask(df, mask, col)
    logging.info("Processed Age...")

    col = "Gender"
    mask = ~df[col].isin(["Male", "Female"])
    process_mask(df, mask, col, replace="Other")
    logging.info("Processed Gender...")

    col = "Blood Type"
    possible_types = ["A+", "A-", "AB+", "AB-", "B+", "B-", "O+", "O-"]
    mask = ~df[col].isin(possible_types)
    process_mask(df, mask, col, replace=None)
    logging.info("Processed Blood Type...")

    col = "Date of Admission"
    df[col] = df[col].apply(convert_to_date)
    mask = df[col].isna()
    process_mask(df, mask, col)
    logging.info("Processed Date of Admission...")

    col = "Doctor"
    mask = df[col].isna()
    process_mask(df, mask, col, replace=None)
    logging.info("Processed Doctor...")

    col = "Hospital"
    mask = df[col].isna()
    process_mask(df, mask, col, replace=None)
    logging.info("Processed Hospital...")

    col = "Room Number"
    df[col] = df[col].apply(convert_to_int)
    mask = df[col].isna()
    process_mask(df, mask, col, replace=0)
    logging.info("Processed Room Number...")

    col = "Admission Type"
    mask = df[col].isna()
    process_mask(df, mask, col)
    logging.info("Processed Admission Type...")

    col = "Discharge Date"
    df[col] = df[col].apply(convert_to_date)
    mask = df[col].isna()
    process_mask(df, mask, col, replace=None)
    logging.info("Processed Discharge Date...")

    col = "Insurance Provider"
    mask = df[col].isna()
    process_mask(df, mask, col, replace=None)
    logging.info("Processed Insurance Provider...")

    col = "Billing Amount"
    df[col] = df[col].apply(convert_to_float).round(2)
    mask = df[col].isna()
    process_mask(df, mask, col)
    logging.info("Processed Billing Amount...")

    col = "Medical Condition"
    mask = df[col].isna()
    process_mask(df, mask, col)
    logging.info("Processed Medical Condition...")

    col = "Medication"
    mask = df[col].isna()
    process_mask(df, mask, col, replace=None)
    logging.info("Processed Medication...")

    col = "Test Results"
    mask = df[col].isna()
    process_mask(df, mask, col)
    logging.info("Processed Test Results...")

    return df

def make_unic_df(df):
    # Handles duplicates by keeping only the latest
    mask = df.duplicated(subset=unic_subset, keep="last")
    duplicated = df[mask].sort_values("Name")
    to_delete = len(duplicated)
    if to_delete:
        logging.warning("Duplicates detected. Only latest is retained, suppressing following elements.")
        logging.warning(duplicated.to_string())
        df.drop(duplicated.index, inplace=True)
    else:
        logging.info("No duplicate detected in the dataset.")
    return df

def migrate_df(df):
    # Main function for migrating DataFrame to MongoDB
    logging.info(f"Execution options - start: {debug_start}, limit: {debug_limit}, traceonly: {debug_traceonly}")
    cnx = get_db()
    logging.info("Cleaning data before migration...")
    df = clean_df(df)
    logging.info("Processing duplicates...")
    df = make_unic_df(df)
    count_inserted = 0
    total = len(df)
    logging.info(f"Total rows after cleaning and merging: {total}")
    for i, row in df.iterrows():
        upsert_row(row.to_dict(), cnx)
        count_inserted += 1
    logging.info(f"Migration complete: {count_inserted} documents inserted out of {total} rows processed.")

def generate_id(rowdict):
    # Concatenate fields, encode as UTF-8, then hash
    unique_string = "_".join(str(rowdict[x]) for x in unic_subset)
    return hashlib.sha256(unique_string.encode("utf-8")).hexdigest()

def upsert_row(rowdict, dbcnx):
    # Transforms a CSV row into a MongoDB document and inserts or updates
    doc = {}
    doc_id = generate_id(rowdict)
    for subdoc, fields in documentmap.items():
        fieldsdoc = {}
        for field in fields:
            camel_field = field[0].lower() + field.title().replace(" ", "")[1:]
            fieldsdoc[camel_field] = rowdict[field]
        doc[subdoc] = fieldsdoc
    logging.debug(f"Document constructed: {doc}")
    if not debug_traceonly:
        try:
            result = dbcnx.care.replace_one({"_id": doc_id}, doc, upsert=True)
            operation = "inserted" if result.upserted_id else "updated"
            logging.info(f"Document {doc_id} {operation}: patient {doc['patient']['Name']} admission {doc['admission']['Date of Admission']}")
        except Exception as e:
            logging.error(f"Error inserting row {e}")
 
    return

def initialize_db(db):
    # Collection initialization and index creation

    # exit function if not first run
    if db_collection_name in db.list_collection_names():
        logging.info(f"Collection {db_collection_name} already exists, no modification applied.")
        return
    try:
        schema_filepath = "data/schema_validation.json"
        with open(schema_filepath, "r") as f:
            schema = json.load(f)
        db.create_collection(db_collection_name, validator=schema)
        logging.info(f"Collection {db_collection_name} created with JSON Schema validation.")
    except pymongo.errors.CollectionInvalid as e:
        logging.error(f"Error creating collection: {e}")
        return
    coll = db[db_collection_name]

    for sdocindex in ["patient.name", "patient.gender", "admission.dateOfAdmission", "admission.hospital", "admission.doctor", "observation.medicalCondition"]:
        try:
            coll.create_index(sdocindex)
            logging.info(f"Index {sdocindex} created.")
        except pymongo.errors.OperationFailure:
            logging.error(f"Failed to create index {sdocindex}.")

    for role in roles:
        try:
            db.command(role)
            logging.info(f"Role {role['createRole']} created.")
        except Exception as e:
            logging.error(f"Error during role {role['createRole']} creation :", e)


def get_db():
    # MongoDB connection via pymongo
    cnxstr = f"mongodb://{username}:{password}@{host}:{port}/"
    client = pymongo.MongoClient(cnxstr)
    dbcnx = client[dbname]
    if not debug_traceonly :
        initialize_db(dbcnx)
        #pass
    return dbcnx

if __name__ == "__main__":
    logging.info("="*50)
    logging.info(f"Starting migration to DB {dbname}")
    hcds = "data/healthcare_dataset.csv"
    df = pd.read_csv(hcds, dtype=str)
    if debug_start or debug_limit:
        df = df.iloc[debug_start:debug_start+debug_limit]
    migrate_df(df)
    logging.info(f"End of migration to DB {dbname}")
    logging.info("")
    logging.info("="*50)
    logging.info("")