from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
import uuid
from ..utils import (
  parse_tag, 
  enforce_required_props, 
  split_props, 
  parse_prop, 
  create_chained_function, 
  fetch_prop, 
  resolve_variable,
  resolve_prop_variables,
  convert_props_to_html
)

register = template.Library()

@register.tag('text_input')
def text_input(parser, token):
  props = token.split_contents()[1:]
  try:
    enforce_required_props(['label'], props)
  except TemplateSyntaxError as e:
    raise TemplateSyntaxError('Error [' + props[0] + ']: ' + str(e))

  props = create_chained_function('onfocus', 'handleTextInputFocus(event);', props)
  props = create_chained_function('onblur', 'handleTextInputBlur(event);', props)

  picked_props, input_props = split_props(['variant', 'label', 'id'], props)

  label = parse_prop(fetch_prop('label', picked_props))[1].replace('\"', '')
  
  variant_prop = fetch_prop('variant', picked_props)
  if variant_prop:
    variant = parse_prop(variant_prop)[1].replace('\"', '')
    if variant != 'text' and variant != 'password':
      variant = 'text'
  else:
    variant = 'text'

  id_prop = fetch_prop('id', picked_props)
  if id_prop:
    id = parse_prop(id_prop)[1].replace('\"', '')
  else:
    id = str(uuid.uuid4())

  return TextInput(variant, label, id, input_props)


class TextInput(Node):
  def __init__(self, variant, label, id, input_props):
    self.variant = variant
    self.label = label
    self.id = id
    self.input_props = input_props

  def render(self, context):
    self.input_props = resolve_prop_variables(self.input_props, context)

    text_input_html = get_template("text_input/index.html")
    context.update({
      'variant': resolve_variable(self.variant, context),
      'label' : resolve_variable(self.label, context),
      'id': resolve_variable(self.id, context)
    })
    foo = text_input_html.render(context).replace('input_props', convert_props_to_html(self.input_props))
    return foo
