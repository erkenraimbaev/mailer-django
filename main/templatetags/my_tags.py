from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter
@register.simple_tag()
def mediapath(value):
    if value:
        return f'/media/{value}'
    else:
        return ''


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
