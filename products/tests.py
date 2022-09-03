from django.test import TestCase
from products.models import Products
from accounts.models import Accounts
from products.ModelSerializers import ProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase,APIClient

class ProductModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        
        cls.seller_username = "Henrique"
        cls.seller_password = "1234"
        cls.seller_first_name = "Henrique"
        cls.seller_last_name = "Ferreira"
        cls.seller_is_seller = True

        cls.seller = Accounts.objects.create_user(username=cls.seller_username, password=cls.seller_password, first_name=cls.seller_first_name, last_name=cls.seller_last_name, is_seller=cls.seller_is_seller)

        cls.description = "Smartband XYZ 3.0"
        cls.price = 100.99
        cls.quantity = 15

        cls.product = Products.objects.create(description=cls.description, price=cls.price, quantity=cls.quantity, seller=cls.seller)

    def test_product_has_information_fields(self):            
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
        self.assertEqual(self.product.seller, self.seller)


class ProductsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super = Accounts.objects.create_superuser(username='super', password='1234', first_name='super', last_name='teste')
        cls.seller = Accounts.objects.create_user(username='usernormal', password='1234', first_name='user', last_name='normal', is_seller=True)
        cls.seller_token = Token.objects.create(user=cls.seller)
        cls.super_token = Token.objects.create(user=cls.super)
        cls.products = [Products.objects.create(description=f'Product {product_id}', price=100.00, quantity=15, seller=cls.seller) for product_id in range(1, 6)]
        cls.products2 = [Products.objects.create(description=f'Product {product_id}', price=100.00, quantity=10, seller=cls.seller) for product_id in range(1, 6)]
        cls.client: APIClient
        cls.base_url = '/api/products/'

    def test_can_retrieve_a_specific_product(self):
        product = self.products[0]
        response = self.client.get(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['description'], product.description)
        self.assertEqual(
            ProductSerializer(instance=product).data,
            response.data
        )


    def test_create_product_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99,
                        "quantity": 15}
        response = self.client.post('/api/products/', product_info)
        expected_response = {"detail": "You do not have permission to create a product."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)


    def test_create_product_without_required_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99}
        response = self.client.post('/api/products/', product_info)
        expected_response = {"quantity": ["This field is required."]}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)