from datetime import datetime
import pandas as pd
import hashlib
import logging
import yaml

PK_ID = "_id"          
DOC = "doc"          
TYPE = "type"         
INDEX = "index"       
PRIMARY = "primary"     
REPLACE = "replace"    
ERROR_MASK = "mask"   
REQUIRED = "required" 

DOCNAME = "care"
ROOT = "root"

def load_yaml(filepath:str):
    with open(filepath, 'r', encoding='utf8') as f:
        return yaml.safe_load(f)

fields_def = load_yaml("data/fields_settings.yml")

class Field():
    """
    Represents a field definition in the dataframe and the MongoDB document.
    """

    dft_values = {DOC : None,
                  TYPE : "str",
                  INDEX : False,
                  PRIMARY : False,
                  REPLACE : False,
                  ERROR_MASK : "is_na",
                  REQUIRED : True,
                  }

    def __init__(self, name, params):
        self.name = name
        self.camel_name = name[0].lower() + name.title().replace(" ", "")[1:]
        self.params = params

    def get_camel_name(self):
        return self.camel_name if self.name != PK_ID else PK_ID
    
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
        self.sdocs = []
        self.convert_dft = None
        self.convert_fmt_date =  "%Y-%m-%d"
        self.float_round = 2

        for fieldname, params in fields_def.items():
            self.fields[fieldname] = Field(fieldname,params)
            sdoc = self.fields[fieldname].get_param(DOC)
            if sdoc not in self.sdocs : 
                self.sdocs.append(sdoc)
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

    def get_schema(self):
        pass
    
    
    def get_doc(self,row:dict):
        """
        Get the MongoDB document representation for a DataFrame row.
        """
        doc={}
        for sdocname in self.sdocs:
            sdoc={}
            for field in self.fields.values():
                field_doc = field.get_param(DOC)
                if  field_doc == sdocname:
                    if field.name == PK_ID:
                        pk_values = "_".join(self.get_pk_values(row))
                        value = hashlib.sha256(pk_values.encode("utf-8")).hexdigest()   
                    else:
                        value = row[field.name]
                    sdoc[field.get_camel_name()] = value
            if sdocname == ROOT:
                doc = sdoc
            else:
                doc[sdocname] = sdoc

        return doc , pk_values

    def get_pk_values(self,row:dict):
        """
        Return a list the primary key values for a MongoDB document.
        """
        pk_values = [str(row[field.name] ) for field in self.fields.values() if field.get_param(PRIMARY)]
        return pk_values

    def get_pk_fields(self):
        """
        Get the primary key fields for a MongoDB document.
        """ 
        return [field.name for field in self.fields.values() if field.get_param(PRIMARY)]
    
    def get_indexes(self):
        """
        Get the index fields for a MongoDB document.
        """
        return [f"{field.get_param(DOC)}.{field.camel_name}" for field in self.fields.values() if field.get_param(INDEX)]
    
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
