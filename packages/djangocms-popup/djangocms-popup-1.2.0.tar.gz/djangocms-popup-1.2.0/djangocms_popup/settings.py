from django.conf import settings
from django.utils.translation import ugettext as _


# add_list_button is content of djangocms_popup_add_list_button or true
ADD_LIST_BUTTON = getattr(settings, "DJANGOCMS_POPUP_ADD_LIST_BUTTON", True)

POPUP_LIST_TEMPLATES = getattr(
    settings, "DJANGOCMS_POPUP_LIST", (("bottom_right.html", _("Bottom right popup")),)
)
