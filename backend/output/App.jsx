import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

const App = () => {
    const [hrEmployees, setHrEmployees] = useState({});
    const [financeBudgets, setFinanceBudgets] = useState({});
    const [inventoryProducts, setInventoryProducts] = useState({});

    const addEmployee = async () => {
        const employeeId = prompt('Enter employee ID:');
        const name = prompt('Enter employee name:');
        const position = prompt('Enter employee position:');
        await axios.post('/api/hr/add', { employeeId, name, position });
        fetchHRData();
    };

    const fetchHRData = async () => {
        const response = await axios.get('/api/hr');
        setHrEmployees(response.data);
    };

    const addBudget = async () => {
        const budgetId = prompt('Enter budget ID:');
        const amount = prompt('Enter budget amount:');
        const description = prompt('Enter budget description:');
        await axios.post('/api/finance/add', { budgetId, amount, description });
        fetchFinanceData();
    };

    const fetchFinanceData = async () => {
        const response = await axios.get('/api/finance');
        setFinanceBudgets(response.data);
    };

    const addProduct = async () => {
        const productId = prompt('Enter product ID:');
        const name = prompt('Enter product name:');
        const stock = prompt('Enter product stock:');
        await axios.post('/api/inventory/add', { productId, name, stock });
        fetchInventoryData();
    };

    const fetchInventoryData = async () => {
        const response = await axios.get('/api/inventory');
        setInventoryProducts(response.data);
    };

    return (
        <div>
            <h1>Mini ERP System</h1>
            <h2>HR Module</h2>
            <button onClick={addEmployee}>Add Employee</button>
            <pre>{JSON.stringify(hrEmployees, null, 2)}</pre>

            <h2>Finance Module</h2>
            <button onClick={addBudget}>Add Budget</button>
            <pre>{JSON.stringify(financeBudgets, null, 2)}</pre>

            <h2>Inventory Module</h2>
            <button onClick={addProduct}>Add Product</button>
            <pre>{JSON.stringify(inventoryProducts, null, 2)}</pre>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));