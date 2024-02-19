from django.db import models

# all it contains is a name which is a character field that represents the programmatic name
# And we'll give that a max length of 254
# And a friendly name which will make that name a little bit more friendly looking for the front end.
# And we'll make it null equals true and blank equals true so that the friendly name is optional.
class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length = 254)
    friendly_name = models.CharField(max_length = 254, null = True, blank = True)
    
    def __str__(self): # string method which takes in the catecory model itself
        return self.name
    
    def get_friendly_name(self): # Same as the string method except this one return the friendly name, if we want it
        return self.friendly_name
    
# null in the database and blank in forms and if a category is deleted we'll set any products that use it to have null for this field
# rather than deleting the product.
class Product(models.Model): 
    category = models.ForeignKey('Category', null = True, blank = True, on_delete = models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True) # Each Product has a sku - optional
    name = models.CharField(max_length=254) # Each Product has a name - REQUIRED
    description = models.TextField() # Each Product has a description - REQUIRED
    price = models.DecimalField(max_digits=6, decimal_places=2) # Each Product has a decimal for price - REQUIRED
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) # Each Product has a decimal for rating - optional
    image_url = models.URLField(max_length=1024, null=True, blank=True) # Each Product has a image URL - optional
    image = models.ImageField(null=True, blank=True) # Each Product has a image field - optional

    def __str__(self):
        return self.name
