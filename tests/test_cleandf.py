# tests/test_convertdf.py
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
## check .test.env START and LIMIT are set to 0 to get full df


from importer.importer import *
from datetime import datetime
import pandas as pd

def test_importer_cleaner():
# same dataset in csv in datapath
   input_dict1= {'Name': {0: 'LesLie TErRy', 1: 'DaNnY sMitH', 2: 'andrEw waTtS', 3: 'adrIENNE bEll'}, 
               'Age': {0: '62', 1: '0' , 2: None, 3: 761}, 
               'Gender': {0: 'Male', 1: 'Unknown', 2: 'female', 3: 'Female'}, 
               'Blood Type': {0: 'A+', 1: 'Z-', 2: 'O+', 3: 'AB'}, 
               'Medical Condition': {0: 'Obesity', 1: 'Obesity', 2: 'Diabetes', 3: 'Cancer'}, 
               'Date of Admission': {0: '2019-08-20', 1: '22-09-22', 2: 45581, 3: '2022-19-19'}, 
               'Doctor': {0: 'Samantha Davies', 1: 'Tiffany Mitchell', 2: 'Kevin Wells', 3: 'Kathleen Hanna'}, 
               'Hospital': {0: 'Kim Inc', 1: 'Cook PLC', 2: 'Hernandez Rogers and Vang,', 3: 'White-White'}, 
               'Insurance Provider': {0: 'Medicare', 1: 'Aetna', 2: 'Medicare', 3: 'Aetna'}, 
               'Billing Amount': {0: '33643.327286577885', 1: '27955.096078842456', 2: '37909.78240987528', 3: '14238.317813937623'}, 
               'Room Number': {0: '265', 1: '205', 2: '450', 3: '458'}, 
               'Admission Type': {0: 'Emergency', 1: 'Emergency', 2: 'Elective', 3: 'Urgent'}, 
               'Discharge Date': {0: '2019-08-26', 1: '2022-10-07', 2: '2020-12-18', 3: '2022-10-09'}, 
               'Medication': {0: 'Ibuprofen', 1: 'Aspirin', 2: 'Ibuprofen', 3: 'Penicillin'}, 
               'Test Results': {0: 'Inconclusive', 1: '', 2: None, 3: 'Abnormal'}}
   
   loaded_df=pd.DataFrame()
   DELETED = "##deleted##"

   def compare(df:pd.Series, wanted_list:list):
      nb = len(wanted_list)
      for index in range(nb):
         wanted_value = wanted_list[index]
         if wanted_value is None:
            if not pd.isna(df[index]):
               return False
         elif wanted_value == DELETED:
            if index in df.index:
               return False
         elif df[index] != wanted_list[index]:
            return False
      return True
   
      #"Age": 
   #     type: int
   #     replace: null
   #     error_mask: 
   #             function: is_inrange
   #             param: [1,120]
                

   #check Age process, 
   field = 'Age'
   df = importer.load_df(input_dict1)
   df = importer.fm.convert_df_values(df,field)
   assert compare(df[field], [62,0, None , 761])
   df = importer.fm.apply_mask(df,field)
   assert compare(df[field], [62,None, None , None])

   #"Gender": 
   #     error_mask: 
   #             function: is_in
   #             param: ["Male", "Female"]
   #     replace: false
   
   field = "Gender"
   df = importer.load_df(input_dict1)
   df = importer.fm.convert_df_values(df,field)
   df = importer.fm.apply_mask(df,field)

   assert compare(df[field], ['Male',DELETED, DELETED , "Female"])
  
#  "Blood Type": 
#        parent: care
#        doc: patient 
#        replace: null 
#        error_mask: 
#                function: is_in
#                param: ["A+", "A-", "AB+", "AB-", "B+", "B-", "O+", "O-"]

   field = "Blood Type"
   df = importer.load_df(input_dict1)
   df = importer.fm.convert_df_values(df,field)
   df = importer.fm.apply_mask(df,field)

   assert compare(df[field], ['A+',None, "O+" , None])

#"Date of Admission": 
#        type: date 
#        replace : False

   field = "Date of Admission"
   df = importer.load_df(input_dict1)
   df = importer.fm.convert_df_values(df,field)
   df = importer.fm.apply_mask(df,field)
   date1 = datetime.strptime('2019-08-20', "%Y-%m-%d")
   assert compare(df[field], [date1, DELETED, DELETED, DELETED])
