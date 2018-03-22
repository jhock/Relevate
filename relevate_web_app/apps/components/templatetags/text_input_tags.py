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
  get_prop_value,
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

  if not fetch_prop('form', props):
    enforce_required_props(['label'], props)

  props = create_chained_function('onfocus', 'handleTextInputFocus(event);', props)
  props = create_chained_function('onblur', 'handleTextInputBlur(event);', props)

  picked_props, input_props = split_props(['variant', 'label', 'id', 'icon', 'input', 'form'], props)
  
  label = get_prop_value('label', picked_props, None)
  input_id = get_prop_value('id', picked_props, str(uuid.uuid4().int))
  icon = get_prop_value('icon', picked_props, None)
  alt_input = get_prop_value('input', picked_props, None)
  alt_form = get_prop_value('form', picked_props, None)
  variant = get_prop_value('variant', picked_props, 'text')

  if variant != 'text' and variant != 'password' and variant != 'email':
    variant = 'text'

  return TextInput(variant, label, input_id, icon, alt_input, alt_form, input_props)


class TextInput(Node):
  def __init__(self, variant, label, input_id, icon, alt_input, alt_form, input_props):
    self.variant = variant
    self.label = label
    self.input_id = input_id,
    self.icon = icon,
    self.alt_input = alt_input,
    self.alt_form = alt_form,
    self.input_props = input_props

  def render(self, context):
    self.input_props = resolve_prop_variables(self.input_props, context)

    text_input_html = get_template("text_input/index.html")
    context.update({
      'variant': resolve_variable(self.variant, context),
      'label' : resolve_variable(self.label, context),
      'id': resolve_variable(self.input_id, context),
      'icon': resolve_variable(self.icon, context),
      'alt_input': resolve_variable(self.alt_input, context),
      'alt_form': resolve_variable(self.alt_form, context)
    })
    markup = text_input_html.render(context)
    return self.process_markup(markup)

  def process_markup(self, markup):
    html_props = convert_props_to_html(self.input_props)
    markup = amend_html_props_to_tag(html_props, markup, 'input')

    if self.alt_input:
      # if the alt input is provided, we need to get the id if it exists
      # and add it to the label as the for attribute
      alt_input_id_prop = get_prop_from_tag('id', markup, 'input')
      if alt_input_id_prop:
        alt_input_id = parse_prop(alt_input_id_prop)[1].replace('\"', '')
        markup = amend_html_props_to_tag('for="' + alt_input_id + '"', markup, 'label')
        markup = amend_html_props_to_tag('class="rv-text-input_input"', markup, 'input')

    if self.alt_form:
      # if the alt form is provided we need to add our attributes to both
      # the label and the input. We trust that the consuming app has set up
      # accessibility attributes properly
      markup = amend_html_props_to_tag('class="rv-text-input_label"', markup, 'label')
      markup = amend_html_props_to_tag('class="rv-text-input_input"', markup, 'input')

    return markup