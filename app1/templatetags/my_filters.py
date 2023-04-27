# Para agregar atributos a los forms de Django de auth_views en templates/registration/
from django import template

register = template.Library()

@register.filter
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')
    for d in definition:
        attr, value = d.split(':')
        attrs[attr.strip()] = value.strip()
    return field.as_widget(attrs=attrs)