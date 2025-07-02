from rest_framework.exceptions import ValidationError

from productservice.models import Category, Product


def convert_fake_store_product_data_to_product(product_data: dict) -> Product:
    if product_data is None:
        print("Received None for product_data")
        raise ValidationError("Product data is invalid")
    category_name = product_data.get('category', 'Unknown')
    category, created = Category.objects.get_or_create(name=category_name)

    # Convert external API data to Django model instance
    product = Product.objects.create(
        title=product_data['title'],
        price=product_data['price'],
        description=product_data.get('description', ''),
        category=category,
    )
    return product


def convert_fake_store_category_data_to_category(category_data: dict) -> Category:

    if isinstance(category_data, str):
        category_name = category_data
        description = ''  # No description available if it's a string
    elif isinstance(category_data, dict):
        category_name = category_data.get('name', 'Unknown')
        description = category_data.get('description', '')
    else:
        raise ValueError(f"Unexpected category_data type: {type(category_data)}")

    # Create or get the category
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        category.description = description
        category.save()

    return category
