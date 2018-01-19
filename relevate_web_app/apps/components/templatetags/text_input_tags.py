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
  convert_props_to_html,
  amend_html_props_to_tag,
  get_prop_from_tag
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

  picked_props, input_props = split_props(['variant', 'label', 'id', 'input'], props)

  label = parse_prop(fetch_prop('label', picked_props))[1].replace('\"', '')
  
  variant_prop = fetch_prop('variant', picked_props)
  if variant_prop:
    variant = parse_prop(variant_prop)[1].replace('\"', '')
    if variant != 'text' and variant != 'password' and variant != 'email':
      variant = 'text'
  else:
    variant = 'text'

  id_prop = fetch_prop('id', picked_props)
  if id_prop:
    input_id = parse_prop(id_prop)[1].replace('\"', '')
  else:
    input_id = str(uuid.uuid4())

  input_prop = fetch_prop('input', picked_props)
  if input_prop:
    alt_input = parse_prop(fetch_prop('input', picked_props))[1]
  else:
    alt_input = None

  if alt_input:
    input_props.append('class="rv-text-input_input"')

  return TextInput(variant, label, input_id, alt_input, input_props)


class TextInput(Node):
  def __init__(self, variant, label, input_id, alt_input, input_props):
    self.variant = variant
    self.label = label
    self.input_id = input_id,
    self.alt_input = alt_input,
    self.input_props = input_props

  def render(self, context):
    self.input_props = resolve_prop_variables(self.input_props, context)

    text_input_html = get_template("text_input/index.html")
    context.update({
      'variant': resolve_variable(self.variant, context),
      'label' : resolve_variable(self.label, context),
      'id': resolve_variable(self.input_id, context),
      'alt_input': resolve_variable(self.alt_input, context)
    })
    html_props = convert_props_to_html(self.input_props)
    markup = text_input_html.render(context)
    markup = amend_html_props_to_tag(html_props, markup, 'input')

    if self.alt_input:
      # if the alt input is provided, we need to get the id if it exists
      # and add it to the label as the for attribute
      alt_input_id_prop = get_prop_from_tag('id', markup, 'input')
      if alt_input_id_prop:
        alt_input_id = parse_prop(alt_input_id_prop)[1].replace('\"', '')
        markup = amend_html_props_to_tag('for="' + alt_input_id + '"', markup, 'label')

    return markup
