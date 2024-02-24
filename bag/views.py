from django.shortcuts import render, redirect 

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):                             # takes both a request and an item id
    """ Add a quantity of the specified product to the shopping bag """
    
    quantity = int(request.POST.get('quantity'))            # get the quantity from the form. Convert it to an integer because it comers from the template as a string
    redirect_url = request.POST.GET('redirect_url')      # Redirect url from the form so we know where to redirect once the process here is finished
    bag = request.session.get('bag', {})                          # Variable bag, accesses the request session. Trying to get this variable if it already exists. And initializing it to an empty dictionary if it doesn't.
    
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
        
    request.session['bag'] = bag
    return redirect(redirect_url)