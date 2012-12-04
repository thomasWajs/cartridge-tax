# -*- coding: utf-8 -*-
from decimal import Decimal

def reverse_vat(cart_item):
    if not cart_item.tax_rate:
        return Decimal('1')
    return Decimal('1') - (Decimal('100.00') / (Decimal('100.00') + cart_item.tax_rate))


def set_salestax(request, tax_type, tax_total):
    """
    Stores the tax type and total in the session.
    """
    request.session["tax_type"] = tax_type
    request.session["tax_total"] = tax_total
