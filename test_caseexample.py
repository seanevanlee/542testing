from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFleetModule(TransactionCase):
    
    def setUp(self):
        # This method is run before each test.
        super(TestFleetModule, self).setUp()
        
        # Create a sample driver for the test
        self.driver = self.env['hr.employee'].create({
            'name': 'John Doe',
            'job_id': self.env.ref('hr.job_driver').id
        })
        
        # Create a sample vehicle model
        self.vehicle_model = self.env['fleet.vehicle.model'].create({
            'name': 'Toyota Prius',
            'brand': 'Toyota',
            'seats': 5,
        })
        
        # Create a sample vehicle
        self.vehicle = self.env['fleet.vehicle'].create({
            'license_plate': 'XYZ1234',
            'driver_id': self.driver.id,
            'model_id': self.vehicle_model.id,
            'odometer': 5000,
        })
    
    def test_create_vehicle(self):
        """ Test creating a new vehicle in the Fleet module """
        
        # Assert that the vehicle is created correctly
        vehicle = self.env['fleet.vehicle'].search([('license_plate', '=', 'XYZ1234')])
        self.assertTrue(vehicle, "Vehicle should be created successfully")
        self.assertEqual(vehicle.license_plate, 'XYZ1234', "Vehicle license plate does not match")
        self.assertEqual(vehicle.driver_id.name, 'John Doe', "Driver name does not match")
        self.assertEqual(vehicle.model_id.name, 'Toyota Prius', "Vehicle model does not match")
    
    def test_odometer_update(self):
        """ Test updating the odometer value of a vehicle """
        
        # Update the vehicle's odometer
        self.vehicle.write({'odometer': 10000})
        
        # Assert that the odometer value is updated correctly
        self.assertEqual(self.vehicle.odometer, 10000, "Odometer value did not update correctly")
    
    def test_vehicle_with_no_driver(self):
        """ Test creating a vehicle with no assigned driver (this should raise an error) """
        
        with self.assertRaises(ValidationError, msg="Driver is required for a vehicle"):
            self.env['fleet.vehicle'].create({
                'license_plate': 'ABC1234',
                'model_id': self.vehicle_model.id,
                'odometer': 10000,
            })
    
    def test_vehicle_status(self):
        """ Test the status change functionality of a vehicle """
        
        # Initially, the vehicle's status should be 'draft'
        self.assertEqual(self.vehicle.state, 'draft', "Initial status should be 'draft'")
        
        # Change the vehicle's state to 'in_service'
        self.vehicle.write({'state': 'in_service'})
        
        # Assert the state has been updated correctly
        self.assertEqual(self.vehicle.state, 'in_service', "Vehicle status did not update to 'in_service'")
        
        # Change the vehicle's state to 'sold'
        self.vehicle.write({'state': 'sold'})
        
        # Assert the state has been updated to 'sold'
        self.assertEqual(self.vehicle.state, 'sold', "Vehicle status did not update to 'sold'")
    
    def test_vehicle_model_relation(self):
        """ Test the relationship between fleet vehicle and its model """
        
        # Create a new vehicle with the model
        vehicle = self.env['fleet.vehicle'].create({
            'license_plate': 'DEF5678',
            'driver_id': self.driver.id,
            'model_id': self.vehicle_model.id,
            'odometer': 20000,
        })
        
        # Assert that the vehicle is correctly related to the model
        self.assertEqual(vehicle.model_id, self.vehicle_model, "Vehicle model relation is incorrect")
        
    def tearDown(self):
        """ This method is run after each test """
        super(TestFleetModule, self).tearDown()
