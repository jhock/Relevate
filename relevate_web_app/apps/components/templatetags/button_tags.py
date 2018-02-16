from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
from ..utils import (
  parse_tag,
  split_props, 
  get_prop_value,
  resolve_variable,
  resolve_prop_variables,
  convert_props_to_html,
  amend_html_props_to_tag,
  replace_tag
)

register = template.Library()

@register.tag('button')
def button(parser, token):
  children, props = parse_tag(parser, token, 'end_button')
  props = token.split_contents()[1:]

  picked_props, button_props = split_props(['variant', 'color', 'fluid_width', 'icon', 'href'], props)

  variant = get_prop_value('variant', picked_props, 'solid')
  color = get_prop_value('color', picked_props, 'primary')
  fluid_width = get_prop_value('fluid_width', picked_props, 'False')
  icon = get_prop_value('icon', picked_props, None)
  href = get_prop_value('href', picked_props, None)

  return Button(children, variant, color, fluid_width, icon, href, button_props)


class Button(Node):
  def __init__(self, children, variant, color, fluid_width, icon, href, button_props):
    self.children = children
    self.variant = variant
    self.color = color
    self.fluid_width = fluid_width if fluid_width == 'True' else None
    self.icon = icon
    self.href = href
    self.button_props = button_props

  def render(self, context):
    self.button_props = resolve_prop_variables(self.button_props, context)

    button_html = get_template("buttons/index.html")
    context.update({
      'children': self.children.render(context),
      'variant': resolve_variable(self.variant, context),
      'color': resolve_variable(self.color, context),
      'fluid_width' : resolve_variable(self.fluid_width, context),
      'icon': resolve_variable(self.icon, context),
      'href': resolve_variable(self.href, context)
    })
    markup = button_html.render(context)
    return self.process_markup(markup, self.href)

  def process_markup(self, markup, href):
    html_props = convert_props_to_html(self.button_props)
    markup = amend_html_props_to_tag(html_props, markup, 'button')
    if href:
      markup = replace_tag(markup, 'button', 'a')

    return markup