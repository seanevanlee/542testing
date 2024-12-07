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
            'gender': 'male',
            'note': 'test case patient'
        })
        
        cls.doctor = cls.env['hospital.doctor'].create({
            'doctor_name': 'Doc Brown',
            'age': 85,
            'gender': 'other'
        })

        # create 2 appointments for John Test patient with Doc Brown
        cls.appointment_1 = cls.env['hospital.appointment'].create({
            'patient_id': cls.patient.id,
            'doctor_id': cls.doctor.id,
            'state': 'done'
        })

        cls.appointment_2 = cls.env['hospital.appointment'].create({
            'patient_id': cls.patient.id,
            'doctor_id': cls.doctor.id
        })
        
    def test_create_patient(self):
        """Test that the patient John Test is created successfully."""
        self.assertTrue(self.patient, "Patient should be created successfully")
        self.assertEqual(self.patient.name, 'John Test', "Name field value is incorrect")
        self.assertEqual(self.patient.gender, 'male', "Gender field value is incorrect")
        self.assertEqual(self.patient.age, 18, "Age is incorrect")

    def test_age_error(self):
        """Test that an error throws when patient age is 0"""
        with self.assertRaises(ValidationError):
            self.patient.age = 0
    
    def test_appointment_count(self):
        """Test that amount of appointments for patient is 2 with compute function"""
        self.assertEqual(self.patient.appointment_count, 2, "Appointment count should be 2")

    def test_unlink_error(self):
        """Test that an error throws if appointment is attempted to be deleted while in done state"""
        with self.assertRaises(ValidationError):
            self.appointment_1.unlink()

    def test_patient_names(self):
        """Test that an error is thrown if patient with a same name is added"""
        with self.assertRaises(ValidationError):
            patient_duplicate = self.env['hospital.patient'].create({
                'name': 'John Test',
                'age': 8,
                'gender': 'female',
            })
