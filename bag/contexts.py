from decimal import Decimal                                                                                   # Import the decimal function
from django.conf import settings                                                                            # Import settings.py file
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    
    bag_items = []                                                                                                        # Empty list for the bag items to live in
    total = 0                                                                                                                   # Eventually need total count when we start adding items to the bag  - - initialized to 0
    product_count = 0                                                                                                  # Eventually need product_count when we start adding items to the bag - - initialized to 0
    bag = request.session.get('bag', {})
    
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            
        })
    
    
    if total < settings.FREE_DELIVERY_THRESHOLD:                                                # Checks whether there is less than 0 items in the back. 
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)   # If it is less we'll calculate delivery as the total multiplied by the standard delivery percentage from settings.py. which in this case is 10%.
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total           # A variable for free delivery - Lets user now how much more they can spend to get free delivery
    else:                                                                                                                           # If the total is greater than or equal to the threshold let's set delivery and the free_delivery_delta to zero.
        delivery = 0
        free_delivery_delta = 0
        
    grand_total = delivery + total                                                                                # to calculate the grand total. All I need to do is add the delivery charge to the total.
        
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    
    return context