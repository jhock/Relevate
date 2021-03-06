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

@register.tag('text_area')
def text_area(parser, token):
  props = token.split_contents()[1:]

  if not fetch_prop('form', props):
    enforce_required_props(['label'], props)

  props = create_chained_function('onfocus', 'handleTextAreaFocus(event);', props)
  props = create_chained_function('onblur', 'handleTextAreaBlur(event);', props)

  picked_props, input_props = split_props(['label', 'description', 'id', 'icon', 'input', 'form'], props)
  
  label = get_prop_value('label', picked_props, None)
  description = get_prop_value('description', picked_props, None)
  input_id = get_prop_value('id', picked_props, str(uuid.uuid4().int))
  alt_input = get_prop_value('input', picked_props, None)
  alt_form = get_prop_value('form', picked_props, None)

  return TextArea(label, description, input_id, alt_input, alt_form, input_props)


class TextArea(Node):
  def __init__(self, label, description, input_id, alt_input, alt_form, input_props):
    self.label = label
    self.description = description
    self.input_id = input_id,
    self.alt_input = alt_input,
    self.alt_form = alt_form,
    self.input_props = input_props

  def render(self, context):
    self.input_props = resolve_prop_variables(self.input_props, context)

    text_area_html = get_template("text_area/index.html")
    context.update({
      'label': resolve_variable(self.label, context),
      'description': resolve_variable(self.description, context),
      'id': resolve_variable(self.input_id, context),
      'alt_input': resolve_variable(self.alt_input, context),
      'alt_form': resolve_variable(self.alt_form, context)
    })
    markup = text_area_html.render(context)
    return self.process_markup(markup)

  def process_markup(self, markup):
    html_props = convert_props_to_html(self.input_props)
    markup = amend_html_props_to_tag(html_props, markup, 'textarea')

    if self.alt_input:
      # if the alt input is provided, we need to get the id if it exists
      # and add it to the label as the for attribute
      alt_input_id_prop = get_prop_from_tag('id', markup, 'textarea')
      if alt_input_id_prop:
        alt_input_id = parse_prop(alt_input_id_prop)[1].replace('\"', '')
        markup = amend_html_props_to_tag('for="' + alt_input_id + '"', markup, 'label')
        markup = amend_html_props_to_tag('class="rv-text-area_input"', markup, 'textarea')

    if self.alt_form:
      # if the alt form is provided we need to add our attributes to both
      # the label and the input. We trust that the consuming app has set up
      # accessibility attributes properly
      markup = amend_html_props_to_tag('class="rv-text-area_label"', markup, 'label')
      markup = amend_html_props_to_tag('class="rv-text-area_input"', markup, 'textarea')

    return markup