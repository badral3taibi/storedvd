from django.test import TestCase

from shop.models import Section, Product, Order, OrderLine


class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Section.objects.create(title='Main', slug='main')
        Product.objects.create(
            title='Title', slug='title',
            section=Section.objects.get(id=1),
            price=200,
            year=2000,
            country='KSA',
            director='Director',
            cast='actors',
            description='Film description'
        )
        Order.objects.create(
            need_delivery=False,
            name='Имя',
            phone='3235235',
            email='abc@example.com',
            address=''
        )
        OrderLine.objects.create(
            order=Order.objects.get(id=1),
            product=Product.objects.get(id=1),
            price=Product.objects.get(id=1).price,
            count=5
        )

    def test_status_choices(self):
        STATUSES = [
            ('NEW', 'New order'),
            ('APR', 'Confirmed'),
            ('PAY', 'Paid'),
            ('CNL', 'Canceled')
        ]
        obj = Order.objects.get(id=1)
        self.assertTrue(obj._meta.get_field('status').choices, STATUSES)

    def test_meta_permissions(self):
        obj = Order.objects.get(id=1)
        permissions = obj._meta.permissions
        self.assertEqual(permissions, (('can_set_status', 'Possibility to customize the status'), ))

    def test_display_products(self):
        obj = Order.objects.get(id=1)
        display_products = obj.display_products()
        self.assertEqual(display_products, 'Title:5 pieces.; ')

    def test_display_amount(self):
        obj = Order.objects.get(id=1)
        display_amount = obj.display_amount()
        self.assertEqual(display_amount, '1000.00 $.')