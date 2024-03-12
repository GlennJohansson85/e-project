import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)                                                          # automatically generate this order number. unique and permanent so users can find their previous orders.
    full_name = models.CharField(max_length=50, null=False, blank=False)                                                                      #
    email = models.EmailField(max_length=254, null=False, blank=False)                                                                           # 
    phone_number = models.CharField(max_length=20, null=False, blank=False)                                                             #
    country = models.CharField(max_length=40, null=False, blank=False)                                                                          #
    postcode = models.CharField(max_length=20, null=True, blank=True)                                                                          # NOT REQUIERED, dont exist in all countries
    town_or_city = models.CharField(max_length=40, null=False, blank=False)                                                                #
    street_address1 = models.CharField(max_length=80, null=False, blank=False)                                                            #
    street_address2 = models.CharField(max_length=80, null=True, blank=True)                                                              #
    county = models.CharField(max_length=80, null=True, blank=True)                                                                              # NOT REQUIERED, dont exist in all countries
    date = models.DateTimeField(auto_now_add=True)                                                                                                      # automatically set the order date and time whenever a new order is created.
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)                                 # calculated using a model method whenever an order is saved.
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)                                   # calculated using a model method whenever an order is saved.#
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)                                  # calculated using a model method whenever an order is saved.#
    original_bag = models.TextField(null=False, blank=False, default='')                                                                             # text field that will contain the original shopping bag that created it.
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')                                                  # character field that will contain the stripe payment intent id which is guaranteed to be unique.
    
    def _generate_order_number(self):                                                                                                                                       #  prepended with an underscore by convention to indicate it's a private method which will only be used inside this class.
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()                                                                                                                                               # generate a random string of 32 characters we can use as an order number.

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0                                     # a method to update the total which we can do using the aggregate function.
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0                                                                                                                                                         # Setting it to zero if the order total is higher than the threshold.
        self.grand_total = self.order_total + self.delivery_cost                                                                                                     # And then to calculate the grand total. add the order total and the delivery cost together and save the instance.
        self.save()                                                                                                                                                                                # Save

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:                                                                                                                                                       #  if the order we're saving right now doesn't have an order number.
            self.order_number = self._generate_order_number()                                                                                                  # We'll call the generate order number method.
        super().save(*args, **kwargs)                                                                                                                                                # And then execute the original save method.

    def __str__(self):                                                                                                                                                                       # string method, returning just the order number 
        return self.order_number                                                                                                                                                      # for the order model.


class OrderLineItem(models.Model):                                                                                                                                                  # Individual shopping bag item. Relating to a specific order and referencing the product itself. The size that was selected. The quantity. And the total cost for that line item.
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)                                                                                    # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity                                                                                                                   # Multiply the product price by the quantity for each line item.
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'                                                                                         # SKU of the product along with the order number it's part of for each order line item.