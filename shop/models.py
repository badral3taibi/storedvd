import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Section(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='Here you need to enter the name of the section',
        unique=True,
        verbose_name='Section name'
    )
    slug = models.SlugField(max_length=40, verbose_name='Nickname', default='')

    class Meta:
        ordering = ['id']
        verbose_name = 'Chapter'
        verbose_name_plural = 'Sections'

    def get_absolute_url(self):
        return reverse('section', args=[self.slug])

    def __str__(self):
        return self.title


class Product(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, verbose_name='Chapter')
    title = models.CharField(max_length=70, verbose_name='Name')
    slug = models.SlugField(max_length=40, verbose_name='Nickname', default='')
    image = models.ImageField(upload_to='images', verbose_name='Image')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)],
        verbose_name='Год'
    )
    country = models.CharField(max_length=70, verbose_name='country')
    director = models.CharField(max_length=70, verbose_name='Director')
    play = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
        verbose_name='Duration',
        help_text='В seconds'
    )
    cast = models.TextField(verbose_name='Cast')
    description = models.TextField(verbose_name='Description')
    date = models.DateField(auto_now_add=True, verbose_name='Date added')

    count = 1

    class Meta:
        ordering = ['title', '-year']
        verbose_name = 'Product'
        verbose_name_plural = 'Goods'

    def get_count(self):
        return self.count

    def get_sum_price(self):
        return self.count * self.price

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.section.title)


class Discount(models.Model):
    code = models.CharField(max_length=10, verbose_name='Coupon code')
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Amount of discount',
        help_text='In percentages'
    )

    class Meta:
        ordering = ['-value']
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def value_percent(self):
        return str(self.value) + '%'

    def __str__(self):
        return self.code + ' (' + str(self.value) + '%)'

    value_percent.short_description = 'Amount of discount'


class Order(models.Model):
    need_delivery = models.BooleanField(verbose_name='Delivery required')
    discount = models.ForeignKey(Discount, verbose_name='Discount', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=70, verbose_name='Name')
    phone = models.CharField(max_length=70, verbose_name='Telephone')
    email = models.EmailField()
    address = models.TextField(blank=True, verbose_name='Address')
    notice = models.TextField(blank=True, verbose_name='Order note')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name='order date')
    date_send = models.DateTimeField(null=True, blank=True, verbose_name='departure date')

    STATUSES = [
        ('NEW', 'New order'),
        ('APR', 'Confirmed'),
        ('PAY', 'Paid'),
        ('CNL', 'Cancelled')
    ]

    status = models.CharField(choices=STATUSES, max_length=3, default='NEW', verbose_name='Статус')

    class Meta:
        ordering = ['-date_order']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        permissions = (('can_set_status', 'Possibility to customize the status'), )

    def display_products(self):
        display = ''
        for order_line in self.orderline_set.all():
            display += '{0}: {1} PC.; '.format(order_line.product.title, order_line.count)
        return display

    def display_amount(self):
        amount = 0
        for order_line in self.orderline_set.all():
            amount += order_line.price * order_line.count

        if self.discount:
            amount = round(amount * Decimal(1 - self.discount.value / 100))
        return '{0} руб.'.format(amount)

    def __str__(self):
        return 'ID: ' + str(self.id)

    display_products.short_description = 'Order list'
    display_amount.short_description = 'Sum'


class OrderLine(models.Model):
    order = models.ForeignKey(Order, verbose_name='Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price', default=0)
    count = models.IntegerField(verbose_name='Quantity', validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = 'Order line'
        verbose_name_plural = 'Order lines'

    def __str__(self):
        return 'Order (ID {0}) {1}: {2} PC.'.format(self.order.id, self.product.title, self.count)
