import unittest
from main import Application

class TestApplication(unittest.TestCase):

    def setUp(self):
        """Set up the test case with a new Application instance."""
        self.app = Application()

    def test_check_in(self):
        """Test checking in a patient."""
        patient = self.app.check_in("John Doe", 30, "Flu symptoms")
        self.assertEqual(patient['name'], "John Doe")
        self.assertEqual(patient['age'], 30)
        self.assertEqual(patient['symptoms'], "Flu symptoms")
        self.assertEqual(patient['status'], "Checked In")
        self.assertEqual(patient['id'], 1)

    def test_get_patient_info(self):
        """Test retrieving patient information."""
        self.app.check_in("Jane Doe", 25, "Cold symptoms")
        patient_info = self.app.get_patient_info(1)
        self.assertEqual(patient_info['name'], "Jane Doe")
        self.assertEqual(patient_info['age'], 25)

    def test_check_out(self):
        """Test checking out a patient."""
        self.app.check_in("John Smith", 45, "Headache")
        checkout_message = self.app.check_out(1)
        self.assertEqual(checkout_message['message'], "Patient checked out successfully")
        self.assertEqual(checkout_message['patient_info']['status'], "Checked Out")
    
    def test_check_out_nonexistent_patient(self):
        """Test checking out a non-existent patient."""
        checkout_message = self.app.check_out(99)
        self.assertEqual(checkout_message['message'], "Patient not found")

    def test_list_patients(self):
        """Test listing patients."""
        self.app.check_in("Alice", 28, "Fever")
        self.app.check_in("Bob", 34, "Broken leg")
        self.app.check_out(1)  # Check out Alice
        patients = self.app.list_patients()
        self.assertEqual(len(patients), 1)
        self.assertEqual(patients[0]['name'], "Bob")

    def test_update_symptoms(self):
        """Test updating patient symptoms."""
        self.app.check_in("Carlos", 22, "Nausea")
        update_response = self.app.update_symptoms(1, "Severe Nausea")
        self.assertEqual(update_response['message'], "Symptoms updated")
        self.assertEqual(update_response['patient_info']['symptoms'], "Severe Nausea")

    def test_update_symptoms_nonexistent_patient(self):
        """Test updating symptoms for a non-existent patient."""
        update_response = self.app.update_symptoms(99, "Nausea")
        self.assertEqual(update_response['message'], "Patient not found")

if __name__ == "__main__":
    unittest.main()