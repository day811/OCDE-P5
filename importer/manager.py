#importer/managerer.py

from datetime import datetime
import pandas as pd
import hashlib
import logging
import yaml

PK_ID = "_id"          
DOC = "doc"
PARENT = "parent"          
TYPE = "type"         
INDEX = "index"       
PRIMARY = "primary"     
REPLACE = "replace"    
ERROR_MASK = "mask"   
REQUIRED = "required" 

ROOT = "root"

def load_yaml(filepath:str, replace=None):
    with open(filepath, 'r', encoding='utf8') as f:
        yml_obj = yaml.safe_load(f)
    if isinstance(replace,dict):
        for placeholer, value in replace.items():
            yml_obj = replace_placeholder(yml_obj,placeholer,value)
    return yml_obj

def replace_placeholder(obj, placeholder, value):
    if isinstance(obj, dict):
        return {k: replace_placeholder(v, placeholder, value) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_placeholder(i, placeholder, value) for i in obj]
    elif isinstance(obj, str) and placeholder in obj:
        return obj.replace(placeholder, value)
    else:
        return obj



class Field():
    """
    Represents a field definition in the dataframe and the MongoDB document.
    """

    dft_values = {
                DOC : None,
                TYPE : "str",
                INDEX : False,
                PRIMARY : False,
                REPLACE : False,
                ERROR_MASK : "is_na",
                REQUIRED : True,
                  }

    def __init__(self, name, params):
        self.name = name
        self.camel_name = (name[0].lower() + name.title().replace(" ", "")[1:]) if self.name != PK_ID else PK_ID
        self.params = params

    def get_param(self, param_name):
        if param_name in self.params:
            return self.params[param_name]
        else:
            return Field.dft_values[param_name]            

class FieldManager():
    """
    Manages field definitions and their transformations.
    """

    def __init__(self):
        """
        Initialize FieldManager with logging and field definitions.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.fields = {}
        self.convert_dft = None
        self.convert_fmt_date =  "%Y-%m-%d"
        self.float_round = 2
        
        fields_def = load_yaml("data/fields_settings.yml")
        for fieldname, params in fields_def.items():
            self.fields[fieldname] = Field(fieldname,params)
        self.log.info(f"Field Manager starts : loading fields params")

    def convert_df_values(self, df:pd.DataFrame,fieldname:str):
        """
        Convert DataFrame column values based on field type.
        """
        ftype = self.fields[fieldname].get_param(TYPE)
        match ftype :
            case "int":
                df[fieldname] = df[fieldname].apply(self.convert_to_int)
            case 'float':
                df[fieldname] = df[fieldname].apply(self.convert_to_float)
            case 'date':
                df[fieldname] = df[fieldname].apply(self.convert_to_date)
        return df
    
    def get_df_error_mask(self,df : pd.DataFrame, fieldname : str):
        """
        Get the error mask for a DataFrame column based on field validation.
        """
        mask_func = self.fields[fieldname].get_param(ERROR_MASK)
        mask = getattr(self,mask_func)(df,fieldname)
        return mask

    def is_na(self,df:pd.DataFrame, fieldname:str):
        """
        Mask missing values in a DataFrame column.
        """
        return df[fieldname].isna()

    def is_age(self, df:pd.DataFrame, fieldname:str):
        """
        Mask invalid age values in a DataFrame column.
        """
        return (df[fieldname] < 0) | (df[fieldname] > 120) | df[fieldname].isna()
    
    def is_gender(self,df:pd.DataFrame, fieldname:str):
        """
        Mask invalid gender values in a DataFrame column.
        """
        return ~df[fieldname].isin(["Male", "Female"])
    
    def is_blood_type(self,df:pd.DataFrame, fieldname:str):
        """
        Mask invalid blood type values in a DataFrame column.
        """
        possible_types = ["A+", "A-", "AB+", "AB-", "B+", "B-", "O+", "O-"]
        return  ~df[fieldname].isin(possible_types)
 
    def apply_mask(self,df:pd.DataFrame, fieldname:str):
        """
        Apply error mask to DataFrame column based on field validation.
        """
        error_mask = self.get_df_error_mask(df,fieldname)
        replace = self.fields[fieldname].get_param(REPLACE) 
        rows_to_log = df[error_mask]
        if len(rows_to_log):
            self.log.warning(f"Incorrect values detected in column {fieldname}.")
            self.log.warning(f"Concerned rows: {rows_to_log}")
            if replace is not False:
                df.loc[error_mask, fieldname] = replace
                self.log.info(f"Replacement of column {fieldname} with {replace} for above rows.")
            else:
                df.drop(df[error_mask].index, inplace=True)
                self.log.info(f"Excluding rows with incorrect values in {fieldname}.")
        else:
            self.log.info(f"No anomaly detected in column {fieldname}.")
        return df

        
    def get_doc(self,row:dict):
        """
        Get the MongoDB document representation for a DataFrame row.
        """
        jsondoc={}

        for field in self.fields.values():
            if field.name == PK_ID:
                document = field.get_param(DOC)
                pk_values = "_".join(self.get_pk_values(row,document))
                value = hashlib.sha256(pk_values.encode("utf-8")).hexdigest()   
            else:
                value = row[field.name]
            
            doc = field.get_param(DOC) 
            parent = field.get_param(PARENT) 
            
            
            if parent == ROOT:
                if doc not in jsondoc.keys(): jsondoc[doc] = {}
                jsondoc[doc][field.camel_name] = value
            else:
                if doc not in jsondoc[parent].keys(): jsondoc[parent][doc] = {}
                jsondoc[parent][doc][field.camel_name] = value


        return jsondoc , pk_values
    

    def get_pk_values(self,row:dict, document):
        """
        Return a list the primary key values for a MongoDB document.
        """
        pk_values = [str(row[field.name] ) for field in self.fields.values() if field.get_param(PRIMARY)== document]
        return pk_values

    def get_pk_fields(self):
        """
        Get the primary key fields for a MongoDB document.
        """ 
        return [field.name for field in self.fields.values() if field.get_param(PRIMARY)]
    
    def get_indexes(self,document_name):
        """
        Get the index fields for a MongoDB document.
        """
        return [f"{field.get_param(DOC)}.{field.camel_name}" for field in self.fields.values() 
                if field.get_param(INDEX) and (field.get_param(DOC) == document_name or field.get_param(PARENT) == document_name)]
    
    def get_masterdoc_list(self):
        return [field.get_param(DOC) for field in self.fields.values() if field.get_param(PARENT) == ROOT]
    
    def convert_to_int(self, val):
        """
        Convert a value to int.
        """
        try:
            return int(val)
        except (ValueError, TypeError) as e:
            self.log.error(f"Error converting to int for value {val}: {e}")
            return self.convert_dft

    def convert_to_float(self, val):
        """
        Convert a value to float.
        """
        try:
            return float(val)  # Compatible with MongoDB
        except (ValueError, TypeError) as e:
            self.log.error(f"Error converting to float for value {val}: {e}")
            return self.convert_dft.round(self.float_round)

    def convert_to_date(self, val):
        """
        Convert a value to date.
        """
        try:
            if pd.isna(val):
                return self.convert_dft
            return datetime.strptime(val, self.convert_fmt_date)
        except (ValueError, TypeError) as e:
            self.log.error(f"Error converting to date for value {val}: {e}")
            return self.convert_dft

    def build_mongodb_schema(self):
        """
        Transform fields dict in mongodb schema
        """
        # Mapping Python type names to MongoDB BSON types
        type_map = {
            'str': 'string',
            'int': 'int',
            'float': 'double',
            'date': 'date'
        }

        def build_properties(node):
            properties = {}
            required = []
            for key, value in node.items():
                # Detect field structure holding 'type' key
                if isinstance(value, dict) and 'type' in value:
                    properties[key] = {'bsonType': type_map.get(value['type'], value['type'])}
                    if value.get('required', False):
                        required.append(key)
                # Nested sub document, recursive call
                elif isinstance(value, dict):
                    sub_properties, sub_required = build_properties(value)
                    properties[key] = {
                        'bsonType': 'object',
                        'properties': sub_properties,
                        'required': sub_required
                    }
                    required.append(key)
            return properties, required

        json_schema = {}
        schema_dict = self.get_mongodb_dict()

        for masterdocname, masterdoc in schema_dict.items():
            properties, required = build_properties(masterdoc)
            json_schema[masterdocname] = {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': required,
                    'properties': properties
                }
            }
        
        return json_schema

    def get_mongodb_dict(self):
        """
        Get hierarchical MongoDB dictionary
        """
        
        needed= [TYPE,REQUIRED]
        jsondoc = {}
        for field in self.fields.values():
            doc = field.get_param(DOC) 
            parent = field.get_param(PARENT) 
            field_params ={}
            for param in needed:
                field_params[param] = field.get_param(param)
            
            if parent == ROOT:
                if doc not in jsondoc.keys(): jsondoc[doc] = {}
                jsondoc[doc][field.camel_name] = field_params
            else:
                if doc not in jsondoc[parent].keys(): jsondoc[parent][doc] = {}
                jsondoc[parent][doc][field.camel_name] = field_params


        return jsondoc 
