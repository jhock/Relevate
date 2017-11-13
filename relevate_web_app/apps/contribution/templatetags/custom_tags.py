from django import template
register = template.Library()

@register.inclusion_tag('components/dropdown-menu.html')
def dropdown_menu():
  return {}