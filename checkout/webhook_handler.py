from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):                                                          # The init method of the class is a setup method that's called every time an instance of the class is created.
        self.request = request                                                               # For us we're going to use it to assign the request as an attribute of the class in case we need to access any attributes of the request coming from stripe.


    def handle_event(self, event):                                                     #  take the event stripe is sending us and simply return an HTTP response indicating it was received.
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
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)


    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)