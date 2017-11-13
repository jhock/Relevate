from django import template
import json

register = template.Library()

@register.inclusion_tag('dropdown_menu.html')
def dropdown_menu(jsonStr):
  menu_props = json.loads(jsonStr)
  return { 'props': menu_props }