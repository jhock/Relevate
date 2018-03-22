from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
from django.utils.html import format_html, escape

from os import listdir
from os.path import dirname, join

from ..utils import (
  enforce_required_props, 
  get_prop_value,
  split_props,
  resolve_variable
)

register = template.Library()

def create_icon(parser, token, variant):
  props = token.split_contents()[1:]

  picked_props, input_props = split_props(['title', 'size', 'color', 'rotate'], props)
  
  title = get_prop_value('title', picked_props, None)
  size = get_prop_value('size', picked_props, 'small')
  color = get_prop_value('color', picked_props, 'dark')
  rotate = get_prop_value('rotate', picked_props, '0')

  return Icon(title, variant, size, color, rotate)

@register.tag('icon_add')
def icon_add(parser, token):
  return create_icon(parser, token, 'add')

@register.tag('icon_arrow')
def icon_arrow(parser, token):
  return create_icon(parser, token, 'arrow')

@register.tag('icon_cloud')
def icon_cloud(parser, token):
  return create_icon(parser, token, 'cloud')

@register.tag('icon_check')
def icon_check(parser, token):
  return create_icon(parser, token, 'check')

@register.tag('icon_circle')
def icon_circle(parser, token):
  return create_icon(parser, token, 'circle')

@register.tag('icon_circle_check')
def icon_circle_check(parser, token):
  return create_icon(parser, token, 'circle_check')

@register.tag('icon_edit')
def icon_edit(parser, token):
  return create_icon(parser, token, 'edit')

@register.tag('icon_save')
def icon_save(parser, token):
  return create_icon(parser, token, 'save')

@register.tag('icon_x')
def icon_x(parser, token):
  return create_icon(parser, token, 'x')

class Icon(Node):
  def __init__(self, title, variant, size, color, rotate):
    self.title = title
    self.variant = variant
    self.size = size
    self.color = color
    self.rotate = rotate

  def render(self, context):
    context.update({
      'title' : resolve_variable(self.title, context)
    })

    try:
      # First, check to see if the template exists
      icon_html = get_template("icons/src/" + resolve_variable(self.variant, context) + ".html")
      icon_markup = icon_html.render(context)
    except:
      icon_markup = None

    container_html = get_template("icons/index.html")
    context.update({
      'icon_markup': icon_markup,
      'size': resolve_variable(self.size, context),
      'color': resolve_variable(self.color, context),
      'rotate': resolve_variable(self.rotate, context)
    })

    return container_html.render(context)
