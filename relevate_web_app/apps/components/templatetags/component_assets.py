from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError

register = template.Library()

@register.inclusion_tag('avatar/assets.html')
def avatar_assets():
  return {}

@register.inclusion_tag('buttons/assets.html')
def button_assets():
  return {}

@register.inclusion_tag('checkbox/assets.html')
def checkbox_assets():
  return {}

@register.inclusion_tag('dropdown_menu/assets.html')
def dropdown_menu_assets():
  return {}

@register.inclusion_tag('file_input/assets.html')
def file_input_assets():
  return {}

@register.inclusion_tag('icons/assets.html')
def icon_assets():
  return {}

@register.inclusion_tag('progress/assets.html')
def progress_assets():
  return {}

@register.inclusion_tag('links/assets.html')
def link_assets():
  return {}

@register.inclusion_tag('select/assets.html')
def select_assets():
  return {}

@register.inclusion_tag('tag/assets.html')
def tag_assets():
  return {}

@register.inclusion_tag('text_area/assets.html')
def text_area_assets():
  return {}

@register.inclusion_tag('text_input/assets.html')
def text_input_assets():
  return {}

@register.inclusion_tag('avatar/assets.html')
def avatar_assets():
  return {}