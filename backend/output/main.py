class Application:
    def __init__(self):
        """
        Initializes the Application with an empty list of patients
        and a counter for patient IDs.
        """
        self.patients = []
        self.patient_id_counter = 1

    def check_in(self, name: str, age: int, symptoms: str) -> dict:
        """
        Checks in a new patient to the emergency room.
        
        Parameters:
            name (str): The name of the patient.
            age (int): The age of the patient.
            symptoms (str): A description of the patient's symptoms.
        
        Returns:
            dict: A dictionary containing the patient's ID and status.
        """
        patient_info = {
            'id': self.patient_id_counter,
            'name': name,
            'age': age,
            'symptoms': symptoms,
            'status': 'Checked In'
        }
        
        self.patients.append(patient_info)
        self.patient_id_counter += 1
        
        return patient_info

    def get_patient_info(self, patient_id: int) -> dict:
        """
        Retrieves information for a specific patient by ID.
        
        Parameters:
            patient_id (int): The ID of the patient.
        
        Returns:
            dict: The patient's information or a message if not found.
        """
        for patient in self.patients:
            if patient['id'] == patient_id:
                return patient
        return {'message': 'Patient not found'}

    def check_out(self, patient_id: int) -> dict:
        """
        Checks out a patient from the emergency room.
        
        Parameters:
            patient_id (int): The ID of the patient to be checked out.
        
        Returns:
            dict: A message indicating the checkout status.
        """
        for patient in self.patients:
            if patient['id'] == patient_id:
                patient['status'] = 'Checked Out'
                return {'message': 'Patient checked out successfully', 'patient_info': patient}
        return {'message': 'Patient not found'}

    def list_patients(self) -> list:
        """
        Lists all currently checked-in patients with their status.
        
        Returns:
            list: A list of patients currently checked in.
        """
        return [patient for patient in self.patients if patient['status'] == 'Checked In']

    def update_symptoms(self, patient_id: int, new_symptoms: str) -> dict:
        """
        Updates the symptoms of a patient based on their ID.
        
        Parameters:
            patient_id (int): The ID of the patient to update.
            new_symptoms (str): The new symptoms description.
        
        Returns:
            dict: The updated patient information or a message if not found.
        """
        for patient in self.patients:
            if patient['id'] == patient_id:
                patient['symptoms'] = new_symptoms
                return {'message': 'Symptoms updated', 'patient_info': patient}
        return {'message': 'Patient not found'}