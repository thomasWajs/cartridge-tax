"""
Checkout process utilities.
"""
from decimal import Decimal


from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings

from cartridge.shop.utils import set_shipping
from cartridge_tax.utils import reverse_vat


def calculate_vat(request):
    tax_total = 0
    for cart_item in request.cart:
        tax_total += cart_item.total_price * reverse_vat(cart_item)
    tax_total = tax_total.quantize(Decimal('0.01'))
    return tax_total

def vat_billship_handler(request, order_form):
    if not request.session.get('free_shipping'):
        settings.use_editable()
        set_shipping(request, _("Flat rate shipping"),
                     settings.SHOP_DEFAULT_SHIPPING_VALUE)

    request.session['tax_total'] = calculate_vat()

def vat_order_handler(request, order_form, order):
    if 'tax_total' in request.session:
        tax_total = request.session['tax_total']
        del request.session['tax_total']
    else:
        tax_total = calculate_vat(request)
    order.tax_total = tax_total
    order.save()
