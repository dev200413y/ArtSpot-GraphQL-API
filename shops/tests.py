from django.test import TestCase
from graphene.test import Client
from .models import Shop
from .schema import schema


class ShopCRUDTestCase(TestCase):
    """
    Test suite covering all CRUD operations for the Shop GraphQL API.
    Tests: Create, Read (list + single), Update, Delete.
    """

    def setUp(self):
        self.client = Client(schema)
        self.shop = Shop.objects.create(
            name="Test Shop",
            email=["test@shop.com", "info@shop.com"],
            phone=["9876543210", "9123456789"],
            address="123 Test Street, Delhi"
        )

    # ─── CREATE ───────────────────────────────────────────────────────────────

    def test_create_shop(self):
        result = self.client.execute(
            """
            mutation {
                createShop(
                    name: "New Shop"
                    email: ["new@shop.com"]
                    phone: ["9000000001"]
                    address: "456 New Street, Mumbai"
                ) {
                    shop {
                        id
                        name
                        email
                        phone
                        address
                    }
                }
            }
            """
        )
        self.assertIsNone(result.get("errors"))
        data = result["data"]["createShop"]["shop"]
        self.assertEqual(data["name"], "New Shop")
        self.assertIn("new@shop.com", data["email"])
        self.assertIn("9000000001", data["phone"])
        self.assertTrue(Shop.objects.filter(name="New Shop").exists())

    # ─── READ ─────────────────────────────────────────────────────────────────

    def test_query_all_shops(self):
        result = self.client.execute(
            """
            query {
                allShops {
                    id
                    name
                    email
                    phone
                    address
                }
            }
            """
        )
        self.assertIsNone(result.get("errors"))
        shops = result["data"]["allShops"]
        self.assertGreaterEqual(len(shops), 1)

    def test_query_single_shop(self):
        result = self.client.execute(
            f"""
            query {{
                shop(id: {self.shop.id}) {{
                    id
                    name
                    email
                    phone
                    address
                }}
            }}
            """
        )
        self.assertIsNone(result.get("errors"))
        data = result["data"]["shop"]
        self.assertEqual(data["name"], "Test Shop")
        self.assertIn("test@shop.com", data["email"])

    def test_query_nonexistent_shop_returns_null(self):
        result = self.client.execute(
            """
            query {
                shop(id: 99999) {
                    id
                    name
                }
            }
            """
        )
        self.assertIsNone(result.get("errors"))
        self.assertIsNone(result["data"]["shop"])

    # ─── UPDATE ───────────────────────────────────────────────────────────────

    def test_update_shop(self):
        result = self.client.execute(
            f"""
            mutation {{
                updateShop(
                    id: {self.shop.id}
                    name: "Updated Shop"
                    email: ["updated@shop.com"]
                ) {{
                    shop {{
                        id
                        name
                        email
                    }}
                }}
            }}
            """
        )
        self.assertIsNone(result.get("errors"))
        data = result["data"]["updateShop"]["shop"]
        self.assertEqual(data["name"], "Updated Shop")
        self.assertIn("updated@shop.com", data["email"])

    def test_update_shop_partial_fields(self):
        """Only updating name should not affect email/phone/address."""
        result = self.client.execute(
            f"""
            mutation {{
                updateShop(id: {self.shop.id}, name: "Partial Update") {{
                    shop {{ name email phone address }}
                }}
            }}
            """
        )
        self.assertIsNone(result.get("errors"))
        data = result["data"]["updateShop"]["shop"]
        self.assertEqual(data["name"], "Partial Update")
        self.assertIn("test@shop.com", data["email"])   # unchanged
        self.assertIn("9876543210", data["phone"])       # unchanged

    def test_update_nonexistent_shop_raises_error(self):
        result = self.client.execute(
            """
            mutation {
                updateShop(id: 99999, name: "Ghost") {
                    shop { id }
                }
            }
            """
        )
        self.assertIsNotNone(result.get("errors"))

    # ─── DELETE ───────────────────────────────────────────────────────────────

    def test_delete_shop(self):
        result = self.client.execute(
            f"""
            mutation {{
                deleteShop(id: {self.shop.id}) {{
                    success
                    message
                }}
            }}
            """
        )
        self.assertIsNone(result.get("errors"))
        data = result["data"]["deleteShop"]
        self.assertTrue(data["success"])
        self.assertFalse(Shop.objects.filter(pk=self.shop.id).exists())

    def test_delete_nonexistent_shop_returns_failure(self):
        result = self.client.execute(
            """
            mutation {
                deleteShop(id: 99999) {
                    success
                    message
                }
            }
            """
        )
        self.assertIsNone(result.get("errors"))
        data = result["data"]["deleteShop"]
        self.assertFalse(data["success"])
        self.assertIn("does not exist", data["message"])
