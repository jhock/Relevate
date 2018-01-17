from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
import uuid
from ..utils import parse_tag, enforce_required_props, split_props, parse_prop, create_chained_function, fetch_prop

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

  input_props_str = ' '.join(str(p) for p in input_props)
  return TextInput(variant, label, id, input_props_str)


class TextInput(Node):
  def __init__(self, variant, label, id, input_props):
    self.variant = variant
    self.label = label
    self.id = id
    self.input_props = input_props

  def render(self, context):
    text_input_html = get_template("text_input/index.html")
    context.update({
      'variant':self.variant,
      'label' : self.label,
      'id': self.id,
      'input_props': self.input_props
    })
    foo = text_input_html.render(context).replace('input_props', self.input_props)
    return foo
