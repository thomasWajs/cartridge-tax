cartridge-vat
=============

VAT Management for Cartridge/Mezzanine

## Installation

Working in your project's [virtualenv](http://www.virtualenv.org/en/latest/index.html):
```
git clone https://github.com/thomasWajs/cartridge-vat.git
cd cartridge-tax
python setup.py install
```

Add `'cartridge_vat'` to your settings.INSTALLED_APPS.

### Billing/Shipping and Order Handlers

Configure your order in the settings, which will add the VAT to each product and to the
order :
```
SHOP_HANDLER_ORDER = "cartridge_vat.checkout.vat_order_handler"
```

If you wish to display the VAT from the shipping step, you can also add :
```
SHOP_HANDLER_BILLING_SHIPPING = \
                "cartridge_vat.checkout.vat_billship_handler"
```

### Extra model fields

Add some extra fields to your settings :
```
EXTRA_MODEL_FIELDS = (
        (
            "cartridge.shop.models.Product.tax_rate",
            "DecimalField",
            (u"Tax Rate",),
            {"null": True, "blank": True, "max_digits": 10, "decimal_places": 2},
        ),
        (
            "cartridge.shop.models.CartItem.tax_rate",
            "DecimalField",
            (u"Tax Rate",),
            {"null": True, "blank": True, "max_digits": 10, "decimal_places": 2},
         ),
        (
            "cartridge.shop.models.OrderItem.tax_rate",
            "DecimalField",
            (u"Tax Rate",),
            {"null": True, "blank": True, "max_digits": 10, "decimal_places": 2},
         ),
        (
            "cartridge.shop.models.Order.tax_total",
            "DecimalField",
            (u"Tax Total",),
            {"null": True, "blank": True, "max_digits": 10, "decimal_places": 2},
        ),
)
```

