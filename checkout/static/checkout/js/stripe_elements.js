/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {                            // Change event - Everytime it changes we´ll check to see if there are errors 32-33
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {                                                                                  // If so we'll display them in the card errors div we created near the card element on the checkout page.
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>`;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');                   // a) After getting the form element the first thing the listener does

form.addEventListener('submit', function(ev) {                                   
    ev.preventDefault();                                                                            // b) is to prevent its default action - In our case is to post
    card.update({ 'disabled': true});                                                          // d) Before we call out to stripe we want to disable the card element  and
    $('#submit-button').attr('disabled', true);                                           // e) the submit button to prevent multiple submissions      
    stripe.confirmCardPayment(clientSecret, {                                       // c) It uses the stripe.confirm card payment method to send the card information securely to stripe.
        payment_method: {                                                                         // f) Call the confirm payment method
            card: card,                                                                                     // g) Provide the card to stripe
        }
    }).then(function(result) {                                                                      // h) Execute this function on the result
        if (result.error) {                                                                                 // i) If there is an error there will be an alert
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);                                                                 // k) re-enable the card element and the submit button to allow the user to fix it. 66 - 68
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {                                                                                                // j) If the status of the payment intent comes back is succeeded we'll submit the form.
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});