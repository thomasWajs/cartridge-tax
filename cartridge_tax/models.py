from cartridge.shop.models import Cart, CartItem, SelectedProduct

def add_item(self, variation, quantity):
    """
    Increase quantity of existing item if SKU matches, otherwise create
    new.
    """
    kwargs = {"sku": variation.sku, "unit_price": variation.price()}
    item, created = self.items.get_or_create(**kwargs)
    if created:
        item.description = unicode(variation)
        item.unit_price = variation.price()
        item.url = variation.product.get_absolute_url()
        image = variation.image
        if image is not None:
            item.image = unicode(image.file)
        variation.product.actions.added_to_cart()
    item.quantity += quantity
    #cartridge_vat addition to original method.
    #Add tax_rate to the cart item
    item.tax_rate = variation.product.tax_rate
    item.save()
Cart.add_item = add_item

#Big hack to add tax_rate to the abstract model SelectedProduct
CartItem._meta.get_field('tax_rate').contribute_to_class(SelectedProduct, 'tax_rate')
