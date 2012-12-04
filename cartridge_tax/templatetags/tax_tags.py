from decimal import Decimal

from django import template

from cartridge.shop.templatetags import shop_tags


register = template.Library()

@register.filter
def currency(value):
    return shop_tags.currency(value)

def _order_totals(context):
    """
    Add ``item_total``, ``shipping_total``, ``discount_total``, ``tax_type``,
    ``tax_total`` and ``order_total`` to the template context. Use the order
    object for email receipts, or the cart object for checkout.
    """
    if "order" in context:
        for f in ("item_total", "shipping_total", "discount_total", "tax_total"):
            context[f] = getattr(context["order"], f)
    else:
        context["item_total"] = context["request"].cart.total_price()
        if context["item_total"] == 0:
            # Ignore session if cart has no items, as cart may have
            # expired sooner than the session.
            context["discount_total"] = context["shipping_total"] = 0
        else:
            for f in ("shipping_type", "shipping_total",
                    "discount_total", "tax_total"):
                context[f] = context["request"].session.get(f, None)
    context["order_total"] = context.get("item_total", None)
    if context.get("shipping_total", None) is not None:
        context["order_total"] += Decimal(str(context["shipping_total"]))
    if context.get("discount_total", None) is not None:
        context["order_total"] -= context["discount_total"]
    return context


@register.inclusion_tag("shop/includes/order_totals.html", takes_context=True)
def order_totals(context):
    """
    HTML version of order_totals.
    """
    return _order_totals(context)


@register.inclusion_tag("shop/includes/order_totals.txt", takes_context=True)
def order_totals_text(context):
    """
    Text version of order_totals.
    """
    return _order_totals(context)
