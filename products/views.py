from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q # If the If the query isn't blank I'm going to use a special object from Jango.db.models called Q to generate a search query.
from .models import Product, Category # display for the user which categories they currently have selected. For that, we need to import category here at the top.

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None # And we'll start with it as none at the top of this view to ensure we don't get an error
    categories = None
    
    if request.GET:
        if 'category' in request.GET: # we'll check whether it exists in requests.get.
            categories = request.GET['category'] # If it does I'm gonna split it into a list at the commas.
            products = products.filter(category__name__in=categories) # And then use that list to filter the current query set of all products down to only products whose category name is in the list.
            categories = Category.objects.filter(name__in=categories) # filter all categories down to the ones whose name is in the list from the URL.
        
        if 'q' in request.GET: # We named the text in the form "q". We can check if q is in request.get
            query = request.GET['q'] # If it is I'll set it equal to a variable called query.
            if not query: # If the query is blank it's not going to return any results
                messages.error(request, "You didn´t enter any search criteria") # So if that's the case let's use the Django messages framework to attach an error message to the request.
                return redirect(reverse('products')) # and then redirect back to the products url
            
            queries = Q(name__icontains = query) | Q(description__icontains = query) #The pipe here is what generates the or statement. And the i in front of contains makes the queries case insensitive. 
            products = products.filter(queries) # Now I can pass them to the filter method in order to actually filter the products.

    context = {
        'products': products,
        'search_term': query, # Now I'll add the query to the context. And in the template call it search term.
        'current_categories': categories, # Let's call that list of category objects, current_categories. and return it to the context so we can use it in the template later on.
    }
        
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)