import unittest
from main import Application, Patient, Appointment

class TestApplication(unittest.TestCase):

    def setUp(self):
        self.app = Application()

    def test_add_patient(self):
        self.app.add_patient("John Doe", "No known allergies")
        patient = self.app.get_patient(0)
        self.assertIsNotNone(patient)
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.medical_history, "No known allergies")

    def test_edit_patient(self):
        self.app.add_patient("Jane Doe", "Asthma")
        self.app.edit_patient(0, "Jane Smith", "Asthma and allergies")
        patient = self.app.get_patient(0)
        self.assertEqual(patient.name, "Jane Smith")
        self.assertEqual(patient.medical_history, "Asthma and allergies")

    def test_schedule_appointment(self):
        self.app.add_patient("Emily Jones", "No medical history")
        self.app.schedule_appointment(0, "2023-10-01 10:00")
        appointment = self.app.get_appointment(0)
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.patient.name, "Emily Jones")
        self.assertEqual(appointment.time_slot, "2023-10-01 10:00")

    def test_record_treatment_notes(self):
        self.app.add_patient("Michael Brown", "Diabetes")
        self.app.schedule_appointment(0, "2023-10-02 11:00")
        self.app.record_treatment_notes(0, "Checked blood sugar levels")
        appointment = self.app.get_appointment(0)
        self.assertIn("Checked blood sugar levels", appointment.notes)

    def test_view_schedule(self):
        self.app.add_patient("Sara Connor", "Healthy")
        self.app.schedule_appointment(0, "2023-10-01 09:00")
        self.app.schedule_appointment(0, "2023-10-01 10:00")
        appointments = self.app.view_schedule("2023-10-01")
        self.assertEqual(len(appointments), 2)

    def test_get_non_existent_patient(self):
        patient = self.app.get_patient(99)
        self.assertIsNone(patient)

    def test_get_non_existent_appointment(self):
        appointment = self.app.get_appointment(99)
        self.assertIsNone(appointment)

if __name__ == '__main__':
    unittest.main()