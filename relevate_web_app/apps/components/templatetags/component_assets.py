from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError

register = template.Library()

@register.inclusion_tag('dropdown_menu/assets.html')
def dropdown_menu_assets():
  return {}

@register.inclusion_tag('buttons/assets.html')
def button_assets():
  return {}

@register.inclusion_tag('links/assets.html')
def link_assets():
  return {}

@register.inclusion_tag('text_input/assets.html')
def text_input_assets():
  return {}