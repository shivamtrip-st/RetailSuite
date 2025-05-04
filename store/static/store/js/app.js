$(document).ready(function() {
    function checkStock(input, increaseBtn, decreaseBtn, addCartButton) {
        const stockQty = parseInt(input.data('stock'));
        let currentQty = parseInt(input.val()) || 1;

        if (stockQty === 0) {
            increaseBtn.hide();
            decreaseBtn.hide();
            addCartButton.hide();
            input.prop('readonly', true);
            $('#stock-status-' + input.data('product-id')).text('Out of Stock').show();
        } else {
            $('#stock-status-' + input.data('product-id')).hide();
            if (currentQty >= stockQty) {
                increaseBtn.prop('disabled', true);
            } else {
                increaseBtn.prop('disabled', false);
            }
            if (currentQty <= 1) {
                decreaseBtn.prop('disabled', true);
            } else {
                decreaseBtn.prop('disabled', false);
            }
            addCartButton.prop('disabled', false);
        }
    }

    $('.qty-cart').each(function() {
        const input = $(this);
        const productId = input.data('product-id');
        const addCartButton = $('#add-cart');
        const increaseBtn = $('#increase-qty-' + productId);
        const decreaseBtn = $('#decrease-qty-' + productId);
        checkStock(input, increaseBtn, decreaseBtn, addCartButton);
    });

    $(document).on('click', '.increase-qty', function () {
        const productId = $(this).data('product-id');
        const input = $('#qty-cart-' + productId);
        const addCartButton = $('#add-cart');
        const increaseBtn = $(this);
        const decreaseBtn = $('#decrease-qty-' + productId);
        const stockQty = parseInt(input.data('stock'));
        let currentQty = parseInt(input.val()) || 1;

        if (currentQty < stockQty) {
            input.val(currentQty + 1);
        }
        checkStock(input, increaseBtn, decreaseBtn, addCartButton);
    });

    $(document).on('click', '.decrease-qty', function () {
        const productId = $(this).data('product-id');
        const input = $('#qty-cart-' + productId);
        const addCartButton = $('#add-cart');
        const increaseBtn = $('#increase-qty-' + productId);
        const decreaseBtn = $(this);
        let currentQty = parseInt(input.val()) || 1;

        if (currentQty > 1) {
            input.val(currentQty - 1);
        }
        checkStock(input, increaseBtn, decreaseBtn, addCartButton);
    });

    $(document).on('input', '.qty-cart', function () {
        const input = $(this);
        const productId = input.data('product-id');
        const addCartButton = $('#add-cart');
        const increaseBtn = $('#increase-qty-' + productId);
        const decreaseBtn = $('#decrease-qty-' + productId);
        checkStock(input, increaseBtn, decreaseBtn, addCartButton);
    });

    $(document).on('click', '#add-cart', function (e) {
        e.preventDefault();
        const productId = $(this).val();
        const qty = $('#qty-cart-' + productId).val();
        const url = $(this).data('url');
        const csrf = $('#csrf_token').val();

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                product_id: productId,
                product_qty: qty,
                csrfmiddlewaretoken: csrf,
                action: 'post'
            },
            success: function (json) {
                if (json.error) {
                    alert(json.error);
                } else {
                    document.getElementById("cart_quantity").textContent = json.qty;
                    location.reload();
                }
            },
            error: function (xhr, errmsg, err) {
                alert("Something went wrong. Please try again!");
            }
        });
    });

    $(document).on('click', '.update-cart', function (e) {
        e.preventDefault();
        const productId = $(this).data('product-id');
        const qty = $('#qty-cart-' + productId).val();
        const url = $(this).data('url');
        const csrf = $('#csrf_token').val();

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                product_id: productId,
                product_qty: qty,
                csrfmiddlewaretoken: csrf,
                action: 'post'
            },
            success: function (json) {
                if (json.error) {
                    alert(json.error);
                } else {
                    document.getElementById("cart_quantity").textContent = json.qty;
                    location.reload();
                }
            },
            error: function (xhr, errmsg, err) {
                alert("Something went wrong while updating the cart.");
            }
        });
    });

    $(document).on('click', '.remove-item', function (e) {
        e.preventDefault();
        const productId = $(this).data('product-id');
        const url = $(this).data('url');
        const csrf = $('#csrf_token').val();

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                product_id: productId,
                csrfmiddlewaretoken: csrf,
                action: 'post'
            },
            success: function (json) {
                location.reload();
            },
            error: function (xhr, errmsg, err) {
                alert("Something went wrong while removing the item.");
            }
        });
    });

});

var toastElList = [].slice.call(document.querySelectorAll('.toast'))
            var toastList = toastElList.map(function (toastEl) {
                var toast = new bootstrap.Toast(toastEl, {
                    autohide: true,
                    delay: 5000
                })
                toast.show()
                return toast
            })
