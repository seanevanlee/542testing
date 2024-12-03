from odoo.tests.common import TransactionCase

class TestFleetAssignDriver(TransactionCase):
    def setUp(self):
        super(TestFleetAssignDriver, self).setUp()
        # Create a sample driver
        self.driver = self.env['res.partner'].create({
            'name': 'Test Driver',
            'email': 'driver@example.com',
        })
        # Create a sample vehicle
        self.vehicle = self.env['fleet.vehicle'].create({
            'name': 'Test Vehicle',
            'license_plate': 'DRIVER123',
            'model_id': self.env['fleet.vehicle.model'].create({
                'name': 'Test Model',
                'brand_id': self.env['fleet.vehicle.model.brand'].create({'name': 'Test Brand'}).id
            }).id
        })

    def test_assign_driver(self):
        """Test assigning a driver to a vehicle"""
        # Assign the driver to the vehicle
        self.vehicle.write({'driver_id': self.driver.id})
        
        # Check if the driver is correctly assigned
        self.assertEqual(
            self.vehicle.driver_id, 
            self.driver, 
            "The driver should be correctly assigned to the vehicle."
        )

    def test_change_driver(self):
        """Test changing the assigned driver for a vehicle"""
        # Create a new driver
        new_driver = self.env['res.partner'].create({
            'name': 'New Test Driver',
            'email': 'new_driver@example.com',
        })
        
        # Assign the new driver
        self.vehicle.write({'driver_id': new_driver.id})
        
        # Check if the new driver is assigned
        self.assertEqual(
            self.vehicle.driver_id, 
            new_driver, 
            "The new driver should be correctly assigned to the vehicle."
        )
