# tests/test_loaddf.py
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
## check .test.env START and LIMIT are set to 0 to get full df


from importer.importer import *
import pandas as pd

def test_importer_loader():
   # same dataset in csv in datapath
    input_dict1= {'Name': {1: 'LesLie TErRy', 2: 'DaNnY sMitH', 3: 'andrEw waTtS', 4: 'adrIENNE bEll'}, 
                'Age': {1: '62', 2: '76', 3: '28', 4: '43'}, 
                'Gender': {1: 'Male', 2: 'Female', 3: 'Female', 4: 'Female'}, 
                'Blood Type': {1: 'A+', 2: 'A-', 3: 'O+', 4: 'AB+'}, 
                'Medical Condition': {1: 'Obesity', 2: 'Obesity', 3: 'Diabetes', 4: 'Cancer'}, 
                'Date of Admission': {1: '2019-08-20', 2: '2022-09-22', 3: '2020-11-18', 4: '2022-09-19'}, 
                'Doctor': {1: 'Samantha Davies', 2: 'Tiffany Mitchell', 3: 'Kevin Wells', 4: 'Kathleen Hanna'}, 
                'Hospital': {1: 'Kim Inc', 2: 'Cook PLC', 3: 'Hernandez Rogers and Vang,', 4: 'White-White'}, 
                'Insurance Provider': {1: 'Medicare', 2: 'Aetna', 3: 'Medicare', 4: 'Aetna'}, 
                'Billing Amount': {1: '33643.327286577885', 2: '27955.096078842456', 3: '37909.78240987528', 4: '14238.317813937623'}, 
                'Room Number': {1: '265', 2: '205', 3: '450', 4: '458'}, 'Admission Type': {1: 'Emergency', 2: 'Emergency', 3: 'Elective', 4: 'Urgent'}, 
                'Discharge Date': {1: '2019-08-26', 2: '2022-10-07', 3: '2020-12-18', 4: '2022-10-09'}, 
                'Medication': {1: 'Ibuprofen', 2: 'Aspirin', 3: 'Ibuprofen', 4: 'Penicillin'}, 
                'Test Results': {1: 'Inconclusive', 2: 'Normal', 3: 'Abnormal', 4: 'Abnormal'}}
    
    #wrong column dictionary
    input_dict2= {'Name': {1: 'LesLie TErRy', 2: 'DaNnY sMitH', 3: 'andrEw waTtS', 4: 'adrIENNE bEll'}, 
                'Age': {1: '62', 2: '76', 3: '28', 4: '43'}, 
                'Gender': {1: 'Male', 2: 'Female', 3: 'Female', 4: 'Female'}, 
                'Blood Type': {1: 'A+', 2: 'A-', 3: 'O+', 4: 'AB+'}, 
                'Medical Condition': {1: 'Obesity', 2: 'Obesity', 3: 'Diabetes', 4: 'Cancer'}, 
                'Date of Admission': {1: '2019-08-20', 2: '2022-09-22', 3: '2020-11-18', 4: '2022-09-19'}, 
                'Doctor': {1: 'Samantha Davies', 2: 'Tiffany Mitchell', 3: 'Kevin Wells', 4: 'Kathleen Hanna'}, 
                'XXXHospital': {1: 'Kim Inc', 2: 'Cook PLC', 3: 'Hernandez Rogers and Vang,', 4: 'White-White'}, 
                'Insurance Provider': {1: 'Medicare', 2: 'Aetna', 3: 'Medicare', 4: 'Aetna'}, 
                'Billing Amount': {1: '33643.327286577885', 2: '27955.096078842456', 3: '37909.78240987528', 4: '14238.317813937623'}, 
                'Room Number': {1: '265', 2: '205', 3: '450', 4: '458'}, 'Admission Type': {1: 'Emergency', 2: 'Emergency', 3: 'Elective', 4: 'Urgent'}, 
                'Discharge Date': {1: '2019-08-26', 2: '2022-10-07', 3: '2020-12-18', 4: '2022-10-09'}, 
                'Medication': {1: 'Ibuprofen', 2: 'Aspirin', 3: 'Ibuprofen', 4: 'Penicillin'}, 
                'Test Results': {1: 'Inconclusive', 2: 'Normal', 3: 'Abnormal', 4: 'Abnormal'}}
    
    loaded_df=pd.DataFrame()

   # test csv 
    csv_filepath = "tests/sample_dataset.csv"
    input_shape = pd.read_csv(csv_filepath,dtype=str).shape
    loaded_df = importer.load_df(csv_filepath)
    output_shape = loaded_df.shape 
    assert output_shape == input_shape
   
   # test input_dict1 
    input_shape = pd.DataFrame(input_dict1).shape
    loaded_df = importer.load_df(input_dict1)
    output_shape = loaded_df.shape 
    assert output_shape == input_shape

    # test input_dict2 : column 'Hospital' missing
    input_shape = pd.DataFrame(input_dict2).shape
    loaded_df = importer.load_df(input_dict2)
    output_shape = loaded_df.shape
    assert output_shape != input_shape

  