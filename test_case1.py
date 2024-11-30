from odoo.tests import common


class TestFleet(common.TransactionCase):

    def setUp(self):
        super(TestFleet, self).setUp()

        brand = self.env["fleet.vehicle.model.brand"].create({
            "name": "Toyota",
        })

        self.brand_name = brand.name

        self.vehicle = self.env["fleet.vehicle.model"].create({
            "brand_id": brand.id,
            "name": "Prius",
            "color": "Red",
            "horsepower" : 200,
            "seats" : 5
        })

    def test_vehicle_model(self):

        print(self.vehicle.color)
        print(self.vehicle.name)

        #msg print only if returns False
        self.assertIsNotNone(self.vehicle.brand_id, "Brand name is missing")
        self.assertEqual(self.brand_name, "Toyota", "Brand name does not match")
        self.assertEqual(self.vehicle.name, "Prius", "Model name does not match")
        self.assertEqual(self.vehicle.color, "Red", "Model color does not match")
        self.assertEqual(self.vehicle.horsepower, 200, "Model horsepower does not match")
        self.assertEqual(self.vehicle.seats, 5, "Model seats does not match")

    def test_vehicle_update(self):

        self.vehicle.update({"color":  "Blue"})
        print(self.vehicle.color)

        self.assertEqual(self.vehicle.color, "Blue", "Vehicle color did not update")

    def tearDown(self):
        """ This method is run after each test """
        super(TestFleet, self).tearDown()
