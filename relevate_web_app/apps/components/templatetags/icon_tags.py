from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
from ..utils import (
  enforce_required_props, 
  get_prop_value,
  split_props,
  resolve_variable
)

register = template.Library()

@register.tag('icon')
def icon(parser, token):
  props = token.split_contents()[1:]
  try:
    enforce_required_props(['title', 'variant'], props)
  except TemplateSyntaxError as e:
    raise TemplateSyntaxError('Error [' + props[0] + ']: ' + str(e))

  picked_props, input_props = split_props(['title', 'variant', 'size', 'color', 'rotate'], props)
  
  title = get_prop_value('title', picked_props, None)
  variant = get_prop_value('variant', picked_props, None)
  size = get_prop_value('size', picked_props, 'small')
  color = get_prop_value('color', picked_props, 'dark')
  rotate = get_prop_value('rotate', picked_props, '0')

  return Icon(title, variant, size, color, rotate)


class Icon(Node):
  def __init__(self, title, variant, size, color, rotate):
    self.title = title
    self.variant = variant
    self.size = size
    self.color = color
    self.rotate = rotate

  def render(self, context):
    icon_html = get_template("icons/src/" + resolve_variable(self.variant, context) + ".html")
    context.update({
      'title' : resolve_variable(self.title, context)
    })
    icon_markup = icon_html.render(context)

    container_html = get_template("icons/index.html")
    context.update({
      'icon_markup': icon_markup,
      'size': resolve_variable(self.size, context),
      'color': resolve_variable(self.color, context),
      'rotate': resolve_variable(self.rotate, context)
    })

    return container_html.render(context)
