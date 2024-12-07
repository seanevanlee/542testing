from odoo.tests import common
from datetime import date


class TestFleet(common.TransactionCase):

    def setUp(self):
        super(TestFleet, self).setUp()

        self.driver = self.env['res.partner'].create({
            'name': 'Test Driver',
            'email': 'driver@example.com',
        })

        brand = self.env["fleet.vehicle.model.brand"].create({
            "name": "Toyota",
        })

        self.vehicle = self.env['fleet.vehicle'].create({
            "id": "12345",
            "model_id": "1",
            "driver_id": self.driver.id
        })

        self.brand_name = brand.name

        self.vehicle_model = self.env["fleet.vehicle.model"].create({
            "brand_id": brand.id,
            "name": "Prius",
            "color": "Red",
            "horsepower": 200,
            "seats": 5,
        })

        self.contract_date = self.env["fleet.vehicle.log.contract"].create({
            "vehicle_id": self.vehicle.id,
            "start_date": date(2022, 4, 30),
            "expiration_date": date(2024, 8, 30),
        })

        self.odometer = self.env['fleet.vehicle.odometer'].create({
            'vehicle_id': self.vehicle.id,
            'value': 1000,
        })

        self.odometer2 = self.env['fleet.vehicle.odometer'].create({
            'vehicle_id': self.vehicle.id,
            'value': 1200,
        })

    def test_vehicle_model(self):
        # msg print only if returns False
        self.assertIsNotNone(self.vehicle_model.brand_id, "Brand name is missing")
        self.assertEqual(self.brand_name, "Toyota", "Brand name does not match")
        self.assertEqual(self.vehicle_model.name, "Prius", "Model name does not match")
        self.assertEqual(self.vehicle_model.color, "Red", "Model color does not match")
        self.assertEqual(self.vehicle_model.horsepower, 200, "Model horsepower does not match")
        self.assertEqual(self.vehicle_model.seats, 5, "Model seats does not match")

    def test_vehicle_update(self):
        self.vehicle_model.write({"color": "Blue"})

        self.assertEqual(self.vehicle_model.color, "Blue", "Vehicle color did not update")

    def test_compute_contract_reminder(self):
        self.overdue = False

        if (self.contract_date.expiration_date - date.today()).days < 0:
            self.overdue = True

        self.assertTrue(self.overdue, "Contract due date did not calculate correctly")

    # test odometer second odometer value entered cannot be less than initial
    def test_odometer_reading(self):
        self.odometer = self.odometer.value
        self.odometer2 = self.odometer2.value

        self.assertEqual(self.odometer, 1000, "Initial odometer value did not get created correctly")
        self.assertEqual(self.odometer2, 1200, "Second odometer value did not get created correctly")
        self.assertGreater(self.odometer2, self.odometer, "Second odometer value entered invalid")

    def test_assign_driver(self):
        # Check if the driver is correctly assigned
        self.assertEqual(
            int(self.vehicle.driver_id),
            self.driver.id,
            "The driver did not get assigned to the vehicle correctly."
        )

        # Check if the new driver is correctly assigned
        self.new_driver = self.env['res.partner'].create({
            'name': 'New Test Driver',
            'email': 'new_driver@example.com',
        })

        self.vehicle.write({
            "driver_id": self.new_driver.id,
        })

        self.assertEqual(
            int(self.vehicle.driver_id),
            self.new_driver.id,
            "The new driver did not get assigned to the vehicle correctly."
        )

def tearDown(self):
    super(TestFleet, self).tearDown()
