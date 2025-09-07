# tests/test_etl.py
from importer.importer import *
import pandas as pd

def test_importer_configuration():
    #source dataset 1
    datapath="dataset1.csv"
    # same dataset in dict
    datadict = {'Name': {1: 'LesLie TErRy', 2: 'DaNnY sMitH', 3: 'andrEw waTtS', 4: 'adrIENNE bEll'}, 
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
    df_datadict = pd.DataFrame(datadict)
    assert importer.load_df(datadict).to_dict() == datadict
    assert importer.load_df(df_datadict).to_dict() == datadict
    assert importer.load_df(datapath).to_dict()== df_datadict