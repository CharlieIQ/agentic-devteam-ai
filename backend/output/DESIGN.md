```python
# main.py

class Application:
    def __init__(self):
        """
        Initializes the mini ERP system application.
        It sets up the different modules (e.g., HR, Finance, Inventory) as empty dictionaries.
        """
        self.modules = {
            "HR": HRModule(),
            "Finance": FinanceModule(),
            "Inventory": InventoryModule(),
        }
    
    def run(self):
        """
        Starts the application and allows selection of modules.
        """
        # Placeholder for future implementation where user can navigate modules

    def get_module(self, module_name: str):
        """
        Retrieves a specific module by name.
        :param module_name: Name of the module to retrieve.
        :return: The requested module instance or None if not found.
        """
        return self.modules.get(module_name, None)


class HRModule:
    def __init__(self):
        """
        Initializes the HR module.
        It keeps track of employees and their details.
        """
        self.employees = {}

    def add_employee(self, employee_id: int, name: str, position: str):
        """
        Adds a new employee to the HR module.
        :param employee_id: Unique identifier for the employee.
        :param name: Name of the employee.
        :param position: Position of the employee in the company.
        """
        self.employees[employee_id] = {
            "name": name,
            "position": position
        }
        
    def remove_employee(self, employee_id: int):
        """
        Removes an employee from the HR module.
        :param employee_id: Unique identifier for the employee to remove.
        """
        if employee_id in self.employees:
            del self.employees[employee_id]

    def get_employee(self, employee_id: int):
        """
        Retrieves an employee's details.
        :param employee_id: Unique identifier for the employee.
        :return: Employee details or None if not found.
        """
        return self.employees.get(employee_id, None)


class FinanceModule:
    def __init__(self):
        """
        Initializes the Finance module.
        It manages budget entries and financial reports.
        """
        self.budgets = {}

    def add_budget(self, budget_id: int, amount: float, description: str):
        """
        Adds a new budget entry.
        :param budget_id: Unique identifier for the budget.
        :param amount: Value of the budget.
        :param description: Description of the budget.
        """
        self.budgets[budget_id] = {
            "amount": amount,
            "description": description
        }

    def remove_budget(self, budget_id: int):
        """
        Removes a budget entry.
        :param budget_id: Unique identifier for the budget to remove.
        """
        if budget_id in self.budgets:
            del self.budgets[budget_id]

    def get_budget(self, budget_id: int):
        """
        Retrieves a budget's details.
        :param budget_id: Unique identifier for the budget.
        :return: Budget details or None if not found.
        """
        return self.budgets.get(budget_id, None)


class InventoryModule:
    def __init__(self):
        """
        Initializes the Inventory module.
        It keeps track of products and their stock levels.
        """
        self.products = {}

    def add_product(self, product_id: int, name: str, stock: int):
        """
        Adds a new product to the inventory.
        :param product_id: Unique identifier for the product.
        :param name: Name of the product.
        :param stock: Available stock for the product.
        """
        self.products[product_id] = {
            "name": name,
            "stock": stock
        }

    def remove_product(self, product_id: int):
        """
        Removes a product from the inventory.
        :param product_id: Unique identifier for the product to remove.
        """
        if product_id in self.products:
            del self.products[product_id]

    def get_product(self, product_id: int):
        """
        Retrieves product details.
        :param product_id: Unique identifier for the product.
        :return: Product details or None if not found.
        """
        return self.products.get(product_id, None)
```

### Implementation Steps for the Engineer:
1. Create a new file named `main.py`.
2. Implement the `Application` class with an `__init__` method to initialize the different modules (HR, Finance, Inventory).
3. For each module, create a corresponding class (`HRModule`, `FinanceModule`, `InventoryModule`) with their own methods for adding, removing, and getting entries.
4. Each class should maintain an appropriate data structure (e.g., dictionary) to hold their respective entries.
5. Implement the `run` method in the `Application` class for user interaction to navigate through modules (to be filled out later).
6. Ensure that method signatures are defined as indicated, with appropriate type hints.
7. Test the module functionalities independently before integrating a UI.

This structured approach provides a self-contained mini ERP system that can be easily expanded with additional features, maintaining clarity and organizational quality.