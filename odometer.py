from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestFleetOdometer(TransactionCase):
    def setUp(self):
        super(TestFleetOdometer, self).setUp()
        # Create a sample vehicle for testing
        self.vehicle = self.env['fleet.vehicle'].create({
            'name': 'Test Vehicle',
            'license_plate': 'TEST123',
            'model_id': self.env['fleet.vehicle.model'].create({
                'name': 'Test Model',
                'brand_id': self.env['fleet.vehicle.model.brand'].create({'name': 'Test Brand'}).id
            }).id
        })

    def test_add_valid_odometer_reading(self):
        """Test adding a valid odometer reading"""
        # Create an odometer reading for the vehicle
        odometer = self.env['fleet.vehicle.odometer'].create({
            'vehicle_id': self.vehicle.id,
            'value': 1000,  # Valid initial reading
        })
        self.assertEqual(odometer.value, 1000, "Odometer reading should be set to 1000.")

        # Add another valid reading
        odometer_2 = self.env['fleet.vehicle.odometer'].create({
            'vehicle_id': self.vehicle.id,
            'value': 1500,  # Valid higher reading
        })
        self.assertEqual(odometer_2.value, 1500, "Odometer reading should be set to 1500.")

    def test_add_invalid_odometer_reading(self):
        """Test adding an invalid odometer reading"""
        # Create a valid initial odometer reading
        self.env['fleet.vehicle.odometer'].create({
            'vehicle_id': self.vehicle.id,
            'value': 1000,
        })

        # Attempt to create a lower reading (invalid)
        with self.assertRaises(ValidationError):
            self.env['fleet.vehicle.odometer'].create({
                'vehicle_id': self.vehicle.id,
                'value': 900,  # Invalid lower reading
            })
