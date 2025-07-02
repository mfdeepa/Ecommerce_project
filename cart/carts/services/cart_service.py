from rest_framework.exceptions import ValidationError, NotFound

from carts.models import Cart, CartItem, Product, Discount

def get_or_create_cart(user_id=None, session_id=None):
    if user_id:
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
    elif session_id:
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    else:
        raise ValidationError("User ID or session ID must be provided.")
    return cart

def add_item_to_cart(cart, product_id, quantity):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise NotFound("Product not found")

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'quantity': quantity,
            'price': product.price
        }
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return cart_item

def update_cart_item_quantity(cart_item_id, quantity):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
    except CartItem.DoesNotExist:
        raise NotFound("Cart item not found")

    if quantity <= 0:
        cart_item.delete()
        return None

    cart_item.quantity = quantity
    cart_item.save()
    return cart_item

def delete_cart_item(cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return True
    except CartItem.DoesNotExist:
        raise NotFound("Cart item not found")

def apply_discount_to_cart(cart, discount_code):
    try:
        discount = Discount.objects.get(code=discount_code)
    except Discount.DoesNotExist:
        raise ValidationError("Invalid discount code.")

    subtotal = cart.get_subtotal()
    if not discount.is_valid(subtotal):
        raise ValidationError("Discount is not valid for current cart subtotal.")

    cart.discount = discount
    cart.save()
    return cart
