from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import ValidationError

@tagged('-standard', 'hospital')

class TestPatient(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestPatient, cls).setUpClass()

        # create the data for each test
        cls.patient = cls.env['hospital.patient'].create({
            'name': 'John Test',
            'age': 18,
            'reference': cls.id,
            'gender': 'male',
            'note': 'test case patient'
        })
        
    def test_create_patient(self):
        """Test that patient is created successfully."""
        self.assertTrue(self.patient, "Patient should be created successfully")
        self.assertEqual(self.patient.name, 'John Test', "Name field value is incorrect")
        self.assertEqual(self.patient.gender, 'male', "Gender field value is incorrect")

    def test_age_error(self):
        """Test that error is thrown when age is 0"""
        with self.assertRaises(ValidationError):
            self.patient.age = 0
    
    def test_appointment_count(self):
        """TODO:Test that amount of appointments for patient is 3 with compute function"""
