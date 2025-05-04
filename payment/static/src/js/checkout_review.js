document.addEventListener("DOMContentLoaded", function () {
    const stripe = Stripe(window.stripe_publishable_key);

    const checkoutButton = document.getElementById("checkout-button");
    if (checkoutButton) {
        checkoutButton.addEventListener("click", function () {
            fetch(window.create_checkout_url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": window.csrf_token
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(session => {
                if (session.error) {
                    console.error(session.error);
                } else {
                    return stripe.redirectToCheckout({ sessionId: session.id });
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    }
});
