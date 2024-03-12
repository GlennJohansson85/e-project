from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False                                                                                                    # 1. Do this assuming the order doesnt exist
        attempt = 1                                                                                                                    # 8. Delay
        while attempt <= 5:                                                                                                        # 9. While loop that will execute up to 5 times
            try:
                order = Order.objects.get(                                                                                   # 2. Then we'll try to get the order using all the information from the payment intent.
                    full_name__iexact=shipping_details.name,                                                  # 3. Using the iexact lookup field (46 -54) to make it an exact match but case-insensitive.
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True                                                                                                # 4. If the order is found
                break                                                                                                                       # 12. If order is found we should break out of the loop
            except Order.DoesNotExist:
                attempt += 1                                                                                                            # 10. Increment attempt by 1
                time.sleep(1)                                                                                                             # 11. Pythons time module to sleep for one second. cause the webhook handler to try to find the order five times over five seconds before giving up and creating the order itself.
        if order_exists:                                                                                                                # 13. Outside the loop, I'll check whether order_exists has been set to true.
            return HttpResponse(                                                                                                # 5. and return a 200 HTTP response to stripe, with the message that we verified the order already exists.
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:                                                                                                                                  # 6. If the order is not found 14 we create the order
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:                                                                                                      # 7. If anything goes wrong the order gets deleted and return a 500 response error to stripe
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)