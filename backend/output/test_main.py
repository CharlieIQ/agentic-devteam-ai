import unittest
from main import Application, HRModule, FinanceModule, InventoryModule

class TestHRModule(unittest.TestCase):
    def setUp(self):
        self.hr = HRModule()

    def test_add_employee(self):
        self.hr.add_employee(1, "Alice", "Engineer")
        self.assertEqual(self.hr.get_employee(1), {"name": "Alice", "position": "Engineer"})

    def test_remove_employee(self):
        self.hr.add_employee(2, "Bob", "Manager")
        self.hr.remove_employee(2)
        self.assertIsNone(self.hr.get_employee(2))

    def test_get_employee_not_found(self):
        self.assertIsNone(self.hr.get_employee(3))

class TestFinanceModule(unittest.TestCase):
    def setUp(self):
        self.finance = FinanceModule()

    def test_add_budget(self):
        self.finance.add_budget(1, 1000.0, "Annual Budget")
        self.assertEqual(self.finance.get_budget(1), {"amount": 1000.0, "description": "Annual Budget"})

    def test_remove_budget(self):
        self.finance.add_budget(2, 500.0, "Marketing Budget")
        self.finance.remove_budget(2)
        self.assertIsNone(self.finance.get_budget(2))

    def test_get_budget_not_found(self):
        self.assertIsNone(self.finance.get_budget(3))

class TestInventoryModule(unittest.TestCase):
    def setUp(self):
        self.inventory = InventoryModule()

    def test_add_product(self):
        self.inventory.add_product(1, "Laptop", 50)
        self.assertEqual(self.inventory.get_product(1), {"name": "Laptop", "stock": 50})

    def test_remove_product(self):
        self.inventory.add_product(2, "Phone", 30)
        self.inventory.remove_product(2)
        self.assertIsNone(self.inventory.get_product(2))

    def test_get_product_not_found(self):
        self.assertIsNone(self.inventory.get_product(3))

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application()

    def test_get_module(self):
        self.assertIsInstance(self.app.get_module("HR"), HRModule)
        self.assertIsInstance(self.app.get_module("Finance"), FinanceModule)
        self.assertIsInstance(self.app.get_module("Inventory"), InventoryModule)

    def test_get_module_not_found(self):
        self.assertIsNone(self.app.get_module("NonExistentModule"))

if __name__ == '__main__':
    unittest.main()