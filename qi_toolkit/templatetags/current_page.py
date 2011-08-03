from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def current_page_link_and_class(request, url, extra_classes=""):
    reverse_str = reverse(url)
    active_str = ""
    if request.path == reverse_str:
        active_str = "current"
    return "href='%s' class='%s %s'" % (reverse_str, active_str, extra_classes)