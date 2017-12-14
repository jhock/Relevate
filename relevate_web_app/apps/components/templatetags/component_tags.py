from django import template
import json

register = template.Library()

@register.inclusion_tag('component_loader.html')
def component_loader(componentName, script):
  return { 
    'componentName': componentName,
    'script': script 
  }

@register.inclusion_tag('dropdown_menu/index.html')
def dropdown_menu(jsonStr):
  menu_props = json.loads(jsonStr)
  return { 'props': menu_props }