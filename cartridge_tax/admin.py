from copy import deepcopy

from django.contrib import admin
from django.db.models import DecimalField

from cartridge.shop.admin import ProductAdmin, OrderAdmin
from cartridge.shop.forms import MoneyWidget, ProductAdminForm
from cartridge.shop.fields import MoneyField
from cartridge.shop.models import Product, Order
from mezzanine.conf import settings

product_fieldsets = deepcopy(ProductAdmin.fieldsets)
product_fieldsets[0][1]["fields"].insert(2, "tax_rate")

class VATProductAdminForm(ProductAdminForm):
    def __init__(self, *args, **kwargs):
        super(VATProductAdminForm, self).__init__(*args, **kwargs)
        self.initial['tax_rate'] = settings.VAT_RATE

class VATProductAdmin(ProductAdmin):
    form = VATProductAdminForm
    fieldsets = product_fieldsets

order_fieldsets = deepcopy(OrderAdmin.fieldsets)
order_fieldsets[2][1]["fields"] = list(order_fieldsets[2][1]["fields"])
order_fieldsets[2][1]["fields"].insert(4, 'tax_total')

class OrderAdmin(OrderAdmin):
    fieldsets = order_fieldsets
    formfield_overrides = {MoneyField: {"widget": MoneyWidget}, DecimalField: {"widget": MoneyWidget}}

admin.site.unregister(Product)
admin.site.register(Product, VATProductAdmin)
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
