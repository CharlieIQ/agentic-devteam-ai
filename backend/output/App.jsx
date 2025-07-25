import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css'; // Assuming you have a styles.css for basic styling

const API_URL = 'http://localhost:5000'; // Adjust if your backend runs on a different port

const App = () => {
    const [patients, setPatients] = useState([]);
    const [appointments, setAppointments] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState(null);
    const [medicalHistory, setMedicalHistory] = useState('');
    const [name, setName] = useState('');
    const [timeSlot, setTimeSlot] = useState('');
    const [notes, setNotes] = useState('');

    useEffect(() => {
        fetchPatients();
        fetchAppointments();
    }, []);

    const fetchPatients = async () => {
        const response = await fetch(`${API_URL}/patients`);
        const data = await response.json();
        setPatients(data);
    };

    const fetchAppointments = async () => {
        const response = await fetch(`${API_URL}/appointments`);
        const data = await response.json();
        setAppointments(data);
    };

    const handleAddPatient = async () => {
        await fetch(`${API_URL}/patients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, medical_history: medicalHistory }),
        });
        fetchPatients();
        setName('');
        setMedicalHistory('');
    };

    const handleScheduleAppointment = async () => {
        await fetch(`${API_URL}/appointments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ patient_id: selectedPatient.id, time_slot: timeSlot }),
        });
        fetchAppointments();
        setTimeSlot('');
    };

    const handleRecordNotes = async (appointmentId) => {
        await fetch(`${API_URL}/appointments/${appointmentId}/notes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ notes }),
        });
        fetchAppointments();
        setNotes('');
    };

    return (
        <div className="app">
            <h1>Dentist Appointment Manager</h1>
            <div>
                <h2>Patients</h2>
                <ul>
                    {patients.map(patient => (
                        <li key={patient.id} onClick={() => setSelectedPatient(patient)}>
                            {patient.name} - {patient.medical_history}
                        </li>
                    ))}
                </ul>
                <input value={name} onChange={e => setName(e.target.value)} placeholder="Patient Name" />
                <input value={medicalHistory} onChange={e => setMedicalHistory(e.target.value)} placeholder="Medical History" />
                <button onClick={handleAddPatient}>Add Patient</button>
            </div>
            {selectedPatient && (
                <div>
                    <h2>Schedule Appointment for {selectedPatient.name}</h2>
                    <input value={timeSlot} onChange={e => setTimeSlot(e.target.value)} placeholder="Time Slot (YYYY-MM-DD HH:MM)" />
                    <button onClick={handleScheduleAppointment}>Schedule Appointment</button>
                    <h2>Previous Appointments</h2>
                    <ul>
                        {appointments.filter(appt => appt.patient.id === selectedPatient.id).map((appt, index) => (
                            <li key={index}>
                                {appt.time_slot}
                                <input value={notes} onChange={e => setNotes(e.target.value)} placeholder="Add Notes" />
                                <button onClick={() => handleRecordNotes(index)}>Add Notes</button>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);