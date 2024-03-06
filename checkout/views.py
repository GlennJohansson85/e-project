from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment") # If there is nothing in the bag the error message will show:
        return redirect(reverse('products'))                                                              # redirect back to the products page

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51OrOQHLNdOdNq26myqf8cNrTM2NQ6bmUVg6wWcmpMMjXVOJRn3ixAeO4FQZX0XAOqNFoOy4VpleDFzGkOynGeLyH00HgZMCprG',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
