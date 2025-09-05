from engine import *
import os
from dotenv import load_dotenv
import logging

load_dotenv(".env")

def get_bool(value):
    return value.lower() in ["true", "1", "yes"]

dockmode = get_bool(os.getenv("DOCKMODE", "0"))

# possibly overwrite CFG in interactive/test mode 
if not dockmode and os.path.exists(".test.env"):
    load_dotenv(".test.env", override=True)

# Loads environment variables from .env
CFG = {
    DBNAME : os.getenv("MONGO_DB_NAME", "test"),
    USERNAME : os.getenv("MONGO_INITDB_ROOT_USERNAME",None),
    PASSWORD : os.getenv("MONGO_INITDB_ROOT_PASSWORD", None),
    HOST : os.getenv("MONGO_HOST", "mongo") if dockmode else "localhost" ,
    PORT: int(os.getenv("MONGO_PORT", 27017)),
    DEBUG_MODE : get_bool(os.getenv("MIGRATION_DEBUG", "0")),
    START : int(os.getenv("DEBUG_START", 0)),
    LIMIT : int(os.getenv("DEBUG_LIMIT", 0)),
    TRACE_ONLY : get_bool(os.getenv("DEBUG_TRACE_ONLY", "1")),
    CLEAN_DB : get_bool(os.getenv("CLEAN_DB", "0")) and not dockmode,
    
}


# Logger configuration
loglvl = logging.INFO if not CFG[DEBUG_MODE] else logging.DEBUG
logging.basicConfig(
    filename="logs/migration_healthcare.log", 
    level=loglvl, 
    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Logger configured")

if not CFG[USERNAME] or not CFG[PASSWORD]:
    logging.critical("Invalid username or password in your .env, must be both filled")
    handle_critical("Consult readme about .env, environment variables and setup process")


importer = Engine(CFG)

if __name__ == "__main__":
    logging.info(STARS)
    logging.info(f"Starting migration to DB {CFG[DBNAME]}")
    
    importer.load_df("data/healthcare_dataset.csv")
    importer.import_df()
    
    logging.info(f"End of migration to DB {CFG[DBNAME]}")
    logging.info(BLANK)
    logging.info(STARS)
    logging.info(BLANK)