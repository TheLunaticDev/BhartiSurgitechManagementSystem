from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    elif isinstance(field, str):
        return mark_safe(field.replace('class="', f'class="{css_class} ', 1))
    else:
        return field