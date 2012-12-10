from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

register_setting(
        name="VAT_RATE",
        label=_("Default VAT Rate"),
        description=_("Tax rate that will be used for new products"),
        editable=True,
        default=19.6,
)
