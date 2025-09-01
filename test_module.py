# test module
import unittest
import migration_script as ms
import pandas as pd




class TestMigrationScript(unittest.TestCase):

    def setUp(self):
        # Création d'un DataFrame test minimal
        data = {
           "Name": ["Alice Smith", "Bob Johnson"],
            "Age": [30, "InvalidAge"],  # 2e ligne invalide pour test
            "Gender": ["Female", "Male"],
            "Blood Type": ["A", "B"],
            "Medical Condition": ["Hypertension", None],
            "Date of Admission": ["2023-01-01", "InvalidDate"],
            "Doctor": ["Dr. House", "Dr. Who"],
            "Hospital": ["General Hospital", "City Clinic"],
            "Insurance Provider": ["Blue Cross", "Medicare"],
            "Billing Amount": [1234.56, "NaN"],
            "Room Number": [101, None],
            "Admission Type": ["Urgent", "Elective"],
            "Discharge Date": ["2023-01-15", None],
            "Medication": ["Aspirin", None],
            "Test Results": ["Normal", "Abnormal"],
        }
        self.df = pd.DataFrame(data)

    
    def test_clean_df(self):
        df_clean = ms.clean_df(self.df)
        # S'assurer que la ligne invalide a été supprimée ou corrigée
        self.assertNotIn("Bob Johnson", df_clean["Name"].values)
        self.assertIn("Alice Smith", df_clean["Name"].values)


if __name__ == "__main__":
    unittest.main()
