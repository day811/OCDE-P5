import pandas as pd
from decimal import Decimal
from datetime import datetime
import pymongo
import os
from dotenv import load_dotenv
import logging
import hashlib
import json


load_dotenv()  # Charge les variables du .env

dockmode = os.getenv("DOCKMODE", "0")
dockmode =dockmode.lower() in ("true", "1", "yes")

db_name = os.getenv("MONGO_DB_NAME", "test")
username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
host = os.getenv("MONGO_HOST", "localhost") if dockmode else "localhost"
port = int(os.getenv("MONGO_PORT", "27017"))
debug_mode = os.getenv("MIGRATION_DEBUG")
debug_mode = debug_mode.lower() in ("true", "1", "yes")

debug_start = int(os.getenv("DEBUG_START"))
debug_limit = int(os.getenv("DEBUG_LIMIT"))

debug_trace_only =os.getenv("DEBUG_TRACE_ONLY")
debug_trace_only = debug_trace_only.lower() in ("true", "1", "yes")

unic_subset = ['Name', 'Gender' , 'Date of Admission','Hospital','Doctor','Medical Condition']
db_collection_name = "care"

# Configuration du logger
log_lvl = logging.INFO if not debug_mode else logging.DEBUG
logging.basicConfig(
    filename='logs/migration_healthcare.log',
    level=log_lvl,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Mapping des champs CSV vers sous-documents MongoDB
document_map = {
    'patient': ['Name', 'Age', 'Gender', "Blood Type"],
    'admission': ['Date of Admission', 'Doctor', 'Hospital', 'Room Number', 'Admission Type', 'Discharge Date'],
    'billing': ['Insurance Provider', 'Billing Amount'],
    'observation': ['Medical Condition', 'Medication', 'Test Results']
}


def process_mask(df, mask, column, replace=False):
    """Gère les valeurs incorrectes en excluant ou remplaçant selon le paramètre replace"""
    rows_to_log = df[mask]
    if len(rows_to_log):
        logging.warning(f"Valeurs incorrectes détectées dans la colonne '{column}'.")
        logging.warning(f"Lignes concernées:\n{rows_to_log}")
        if replace is not False:
            df.loc[mask, column] = replace
            logging.info(f"Remplacement de la colonne '{column}' par '{replace}' pour les lignes ci-dessus.")
        else:
            df.drop(df[mask].index, inplace=True)
            logging.info(f"Exclusion des lignes avec des valeurs incorrectes dans '{column}'.")
    else:
        logging.info(f"Aucune anomalie détectée dans la colonne '{column}'.")

def convert_to_int(val, dft=None):
    try:
        return int(val)
    except (ValueError, TypeError) as e:
        logging.error(f"Erreur conversion int pour valeur '{val}': {e}")
        return dft

def convert_to_float(val, dft=None):
    try:
        return float(val)  # Compatible MongoDB
    except (ValueError, TypeError) as e:
        logging.error(f"Erreur conversion float pour valeur '{val}': {e}")
        return dft

def convert_to_date(val, format='%Y-%m-%d', dft=None):
    try:
        if pd.isna(val):
            return dft
        return datetime.strptime(val, format)
    except (ValueError, TypeError) as e:
        logging.error(f"Erreur conversion date pour valeur '{val}': {e}")
        return dft

def clean_df(df):
    """Nettoie et valide le dataframe"""
    # Name
    col = 'Name'
    mask = df[col].isna()
    process_mask(df, mask, col)

    # Age
    col = 'Age'
    df[col] = df[col].apply(convert_to_int)
    mask = (df[col] < 0) | (df[col] > 120) | (df[col].isna())
    process_mask(df, mask, col)

    # Gender
    col = 'Gender'
    mask = ~df[col].isin(["Male", "Female"])
    process_mask(df, mask, col, replace="Other")

    # Blood Type
    col = 'Blood Type'
    possible_types = ["A+", "A-", "AB+", "AB-", "B+", "B-", "O+", "O-"]
    mask = ~df[col].isin(possible_types)
    process_mask(df, mask, col, replace="NA")

    # Date of Admission
    col = 'Date of Admission'
    df[col] = df[col].apply(convert_to_date)
    mask = df[col].isna()
    process_mask(df, mask, col)

    # Doctor
    col = "Doctor"
    mask = df[col].isna()
    process_mask(df, mask, col, replace="NA")

    # Hospital
    col = "Hospital"
    mask = df[col].isna()
    process_mask(df, mask, col, replace="NA")

    # Room Number
    col = "Room Number"
    df[col] = df[col].apply(convert_to_int)
    mask = df[col].isna()
    process_mask(df, mask, col, replace=0)

    # Admission Type
    col = "Admission Type"
    mask = df[col].isna()
    process_mask(df, mask, col)

    # Discharge Date
    col = 'Discharge Date'
    df[col] = df[col].apply(convert_to_date)
    mask = df[col].isna()
    process_mask(df, mask, col, replace=None)

    # Insurance Provider
    col = "Insurance Provider"
    mask = df[col].isna()
    process_mask(df, mask, col, replace="NA")

    # Billing Amount
    col = "Billing Amount"
    df[col] = df[col].apply(convert_to_float).round(2)
    mask = df[col].isna()
    process_mask(df, mask, col)

    # Medical Condition
    col = "Medical Condition"
    mask = df[col].isna()
    process_mask(df, mask, col)

    # Medication
    col = "Medication"
    mask = df[col].isna()
    process_mask(df, mask, col, replace="NA")

    # Test Results
    col = "Test Results"
    mask = df[col].isna()
    process_mask(df, mask, col)

    return df

def make_unic(df):
    """Gère les doublons en ne gardant que le dernier"""
    mask = df.duplicated(subset=unic_subset, keep='last')
    #df = df[~mask].sort_values(['Name'])if 'Age' in subset_cols:
    duplicated = df[mask]
    to_delete = len(duplicated)
    if to_delete:
        logging.warning(f"Doublons détectés. Traitement du seul dernier, suppression des {to_delete} éléments suivants.")
        logging.warning(duplicated.to_string())
        df.drop(df[mask].index, inplace=True)
    else:
        logging.info("Aucun doublon détecté dans le dataset.")
    return df

def migrate_df(df):
    """Fonction principale de migration du DataFrame vers MongoDB"""
    logging.info(f"Options d'exécution - start : {debug_start} limit:{debug_limit} trace_only:{debug_trace_only}")


    cnx = get_db()

    logging.info(f"Nettoyage des données avant migration...")
    df = clean_df(df)

    logging.info(f"Traitement des doublons...")
    df = make_unic(df)

    count_inserted = 0
    total = len(df)
    logging.info(f"Total lignes après nettoyage et fusion : {total}")

    for i, row_dict in df.iterrows():
        try:
            upsert_row(row_dict.to_dict(), cnx)
            count_inserted += 1
        except Exception as e:
            logging.error(f"Erreur lors de l’insertion de la ligne {i}: {e}")

    logging.info(f"Migration terminée : {count_inserted} documents insérés sur {total} lignes traitées.")

def generate_id(row_dict):
    # Concaténation des champs, encodée en UTF-8 puis hashée
    unique_string = "".join(str(row_dict[x]) for x in unic_subset)
    return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

def upsert_row(row_dict, db_cnx):
    """Transforme une ligne CSV en document MongoDB et l'insère ou  la met à jour"""
    doc = {}
    doc["_id"] = generate_id(row_dict)
    for subdoc, fields in document_map.items():
        fields_doc = {}
        for field in fields:
            fields_doc[field] = row_dict[field]
        doc[subdoc] = fields_doc
    logging.debug(f"Document construit : {doc}")

    if not debug_trace_only:
        #db_cnx.care.insert_one(doc)
        result = db_cnx.care.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        operation = 'inséré' if result.upserted_id else 'mis à jour'
        logging.info(f"Document {doc['_id']} {operation} : patient {doc['patient']['Name']} admission {doc['admission']['Date of Admission']}")

def initialize_db(db):
    if db_collection_name in db.list_collections():
        logging.info(f"Collection '{db_collection_name}' existe déjà, aucune modification appliquée.")
        # pas d'action : on arrête
        return
    try:
        schema_file_path="data/schema_validation.json"
        with open(schema_file_path, 'r') as f:
            schema = json.load(f)
        db.create_collection(db_collection_name, validator=schema)
        logging.info(f"Collection '{db_collection_name}' créée avec validation JSON Schema.")
    except pymongo.errors.CollectionInvalid as e:
        logging.error(f"Erreur création collection : {e}")

    coll = db[db_collection_name]
    # Création des index seulement à la création
    for sdoc_index in ["patient.Name","admission.Doctor","billing.Insurance Provider"]:
        try:
            coll.create_index(sdoc_index)
            logging.info(f"Index '{sdoc_index}' créé.")
        except pymongo.errors.OperationFailure:
            logging.error(f"Echec de la création de l'index'{sdoc_index}'.")
    

def get_db():
    """Connexion MongoDB via pymongo"""
    cnx_str = f"mongodb://{username}:{password}@{host}:{port}/"
    client = pymongo.MongoClient(cnx_str)
    db_cnx = client[db_name]
    initialize_db(db_cnx)
    return db_cnx

if __name__ == "__main__":
    logging.info("*" * 50)
    logging.info("")
    logging.info(f"Démarrage de la migration vers la DB : {db_name}")

    hcds = "data/healthcare_dataset.csv"
    df = pd.read_csv(hcds, dtype=str)
    if debug_start > 0 or debug_limit >0:
        df = df.iloc[debug_start:debug_start+debug_limit]
    migrate_df(df)  # prend en compte les var d'environnement pour lancer le script
    logging.info(f"Fin de la migration vers la DB : {db_name}")
    logging.info("")
    logging.info("*" * 50)
    logging.info("")

