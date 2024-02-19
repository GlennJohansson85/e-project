from django.shortcuts import render
from .models import Product # import product model.

# Create your views here.
def all_products(request):
    # view to show all products, including sorting and search queries
    
    products = Product.objects.all() # Return all products from the database
        
    context = {    # Add the same (line 8) to the context so the products  will be available in the template.
        'products' : products,
    }
    
    return render(request, "products/products.html", context) # Context needed to send things back to the template