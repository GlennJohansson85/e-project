from django import forms
from .models import Order # import our order model


class OrderForm(forms.ModelForm): # Meta options telling django which model itll be associated with and which fields we want to render
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs): # override the init method of the form which will allow us to customize it quite a bit.
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)           # First we call the default init method to set the form up as it would be by default.
        placeholders = {                                        #  I've created a dictionary of placeholders which will show up in the form fields rather than having clunky looking labels and empty text boxes in the template.
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True       # Next we're setting the autofocus attribute on the full name field to true so the cursor will start in the full name field when the user loads the page.
        for field in self.fields:                                                                # finally we iterate through the forms fields
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'                           # adding a star to the placeholder if it's a required field on the model.
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder # Setting all the placeholder attributes to their values in the dictionary above.
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'   # Adding a CSS class we'll use later.
            self.fields[field].label = False                                                  # And then removing the form fields labels. Since we won't need them given the placeholders are now set.