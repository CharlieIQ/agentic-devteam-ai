import React, { useState, useEffect } from 'react';  
import ReactDOM from 'react-dom';  
import './index.css';  
import { Application } from './main.py'; // Import the Application class from main.py

const App = () => {  
    const [patients, setPatients] = useState([]);  
    const [name, setName] = useState('');  
    const [age, setAge] = useState('');  
    const [symptoms, setSymptoms] = useState('');  
    const [checkOutId, setCheckOutId] = useState('');  
    const [message, setMessage] = useState('');  

    const application = new Application();

    const checkIn = () => {  
        const patient = application.check_in(name, parseInt(age), symptoms);  
        setPatients([...patients, patient]);  
        setMessage(`Patient ${patient.name} checked in!`);  
        setName('');  
        setAge('');  
        setSymptoms('');  
    };  

    const checkOut = () => {  
        const response = application.check_out(parseInt(checkOutId));  
        if (response.message === 'Patient checked out successfully') {  
            setPatients(patients.filter(patient => patient.id !== parseInt(checkOutId)));  
        }  
        setMessage(response.message);  
        setCheckOutId('');  
    };  

    useEffect(() => {  
      setPatients(application.list_patients());  
    }, [application]);  

    return (  
        <div>  
            <h1>Emergency Room App</h1>  
            <div>  
                <h2>Check In Patient</h2>  
                <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />  
                <input type="number" placeholder="Age" value={age} onChange={(e) => setAge(e.target.value)} />  
                <input type="text" placeholder="Symptoms" value={symptoms} onChange={(e) => setSymptoms(e.target.value)} />  
                <button onClick={checkIn}>Check In</button>  
            </div>  
            <div>  
                <h2>Patients List</h2>  
                <ul>  
                    {patients.map(patient => (  
                        <li key={patient.id}>  
                            {patient.name} (ID: {patient.id}, Status: {patient.status})  
                        </li>  
                    ))}  
                </ul>  
            </div>  
            <div>  
                <h2>Check Out Patient</h2>  
                <input type="number" placeholder="Patient ID" value={checkOutId} onChange={(e) => setCheckOutId(e.target.value)} />  
                <button onClick={checkOut}>Check Out</button>  
            </div>  
            {message && <div><strong>{message}</strong></div>}  
        </div>  
    );  
};  

ReactDOM.render(<App />, document.getElementById('root'));