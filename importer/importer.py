#importer/importer.py

from importer.engine import *
import os
from dotenv import load_dotenv
import logging

load_dotenv(".env")

def get_bool(value):
    return value.lower() in ["true", "1", "yes"]

dockmode = get_bool(os.getenv("DOCKMODE", "0"))
dbname = prod_dbname = os.getenv("MONGO_DB_NAME","healthcare")

# possibly overwrite CFG in interactive/test mode 
if not dockmode and os.path.exists(".test.env"):
    load_dotenv(".test.env", override=True)
    # ensure dbname in test mode is different from dock mode
    dbname = os.getenv("MONGO_DB_NAME", "healthcare")
    if dbname == prod_dbname:
        dbname = f"test{prod_dbname}"

# Loads environment variables from `.env`(+`.test.env`)
CFG = {
    DBNAME : dbname,
    USERNAME : os.getenv("MONGO_INITDB_ROOT_USERNAME",None),
    PASSWORD : os.getenv("MONGO_INITDB_ROOT_PASSWORD", None),
    HOST : os.getenv("MONGO_HOST", "mongo") if dockmode else "localhost" ,
    PORT: int(os.getenv("MONGO_PORT", 27017)),
    DEBUG_MODE : get_bool(os.getenv("MIGRATION_DEBUG", "0")),
    START : int(os.getenv("START", 0)),
    LIMIT : int(os.getenv("LIMIT", 0)),
    TRACE_ONLY : get_bool(os.getenv("DEBUG_TRACE_ONLY", "1")) and not dockmode,
    CLEAN_DB : get_bool(os.getenv("CLEAN_DB", "0")) and not dockmode,  # ONLY IN TEST MODE !!!
    PROD_DBNAME : prod_dbname,
    DOCKMODE : dockmode,
}


# Logger configuration
loglvl = logging.INFO if not CFG[DEBUG_MODE] else logging.DEBUG
logging.basicConfig(
    filename="logs/migration_healthcare.log", 
    level=loglvl, 
    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Logger configured")

if not CFG[USERNAME] or not CFG[PASSWORD]:
    logging.critical("Invalid username and/or password in your .env, must be both filled")
    handle_critical("Consult readme about .env, environment variables and setup process")


importer = Engine(CFG)

if __name__ == "__main__":
    logging.info(STARS)
    logging.info(f"Starting migration to DB {CFG[DBNAME]}")
    logging.info(f"Running environment : {'PRODUCTION' if dockmode else 'TESTING'}")
    
    importer.load_df("data/healthcare_dataset.csv")
    importer.import_df()
    
    logging.info(f"End of migration to DB {CFG[DBNAME]}")
    logging.info(BLANK)
    logging.info(STARS)
    logging.info(BLANK,BLANK,BLANK)