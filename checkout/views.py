from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents                                                          # a) Import the bag contents function from bag.context. Makes that function available for use here in our views.

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():                                                                                    # 1. If order is valid
            order = order_form.save()                                                                           # 2.  We save the order
            for item_id, item_data in bag.items():                                                        # 3. Iterate through the bag items to create each line item
                try:
                    product = Product.objects.get(id=item_id)                                         # 1. Product ID out of the bag
                    if isinstance(item_data, int):                                                                 # 2. if value is an integer we know we're working with an item that doesn't have sizes.
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,                                                                      # 3. the quantity will just be the item data.
                        )
                        order_line_item.save()
                    else:                                                                                                          # 4. Otherwise, if the item has sizes
                        for size, quantity in item_data['items_by_size'].items():                # 5. we'll iterate through each size and create a line item accordingly.
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:                                                                     # 6. If a product isnt found
                    messages.error(request, (                                                                       # 7. We´ll add an error message saying:
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()                                                                                             # 8. Delete the empty order
                    return redirect(reverse('view_bag'))                                                        # 9. And return the user to the shopping bag

            request.session['save_info'] = 'save-info' in request.POST                             # 10. If the user wants to safe their profile information for this session
            return redirect(reverse('checkout_success', args=[order.order_number])) # 11.  And then redirect them to a new page
        else:                                                                                                                          # If the order form is invalid we provide them with the form errors shown
            messages.error(request, 'There was an error with your form. \
            Please double check your information.')
    else:
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


def checkout_success(request, order_number):                                                   # take the order number and render a nice success page letting the user know that their payment is complete.
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')                                                      # 1. Check whether the user wanted to save their information by getting that from the session just like we get the shopping bag.
    order = get_object_or_404(Order, order_number=order_number)              # 2. use the order number to get the order created in the previous view which we´ll send back to the template
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')                                                                # 3. Line 102 - 104: Then I'll attach a success message letting the user know what their order number is.

    if 'bag' in request.session:                                                                                    # 4. Finally, I'll delete the user shopping bag from the session since it'll no longer be needed for this session.
        del request.session['bag']

    template = 'checkout/checkout_success.html'                                                 # 5. Set the template and the context.
    context = {
        'order': order,
    }

    return render(request, template, context)                                                         # 6. And render the template.