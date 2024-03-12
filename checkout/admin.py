from django.contrib import admin
from .models import Order, OrderLineItem # imported models


class OrderLineItemAdminInline(admin.TabularInline): # inherit from TabularInline = allow us to add and edit line items in the admin right from inside the order model.
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin): 
    inlines = (OrderLineItemAdminInline,) # Making the "line item total" to a readonly

    readonly_fields = ('order_number', 'date', # These fields are all things that will be calculated by our model methods. don't want anyone to have the ability to edit them since it could compromise the integrity of an order.
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag', 'stripe_pid')

    fields = ('order_number', 'date', 'full_name', # Fields options -Order stays the same as it appears in the model
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag', 'stripe_pid')

    list_display = ('order_number', 'date', 'full_name', # To restrict the columns that show up in the order list to only a few key items. And I'll set them to be ordered by date in reverse chronological order putting the most recent orders at the top.
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',) #  ordered by date in reverse chronological order putting the most recent orders at the top.

admin.site.register(Order, OrderAdmin) # Skipping register the OrderLineItem model cos its accessible via the inline on the order model.