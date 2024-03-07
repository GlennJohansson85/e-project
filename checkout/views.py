from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents                                                          # a) Import the bag contents function from bag.context. Makes that function available for use here in our views.

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment") # If there is nothing in the bag the error message will show:
        return redirect(reverse('products'))                                                              # redirect back to the products page

    current_bag = bag_contents(request)                                                            # b) Store it in a variable called current_bag making sure to to overwrite the bag variable that already exists
    total = current_bag['grand_total']                                                                   # c) To get the total all I need to do is get the grand_total key out of the current bag.
    stripe_total = round(total * 100)                                                                        # d) Multiply that by a hundred and round it to zero decimal places using the round function. Since stripe will require the amount to charge as an integer.
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    
    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)