from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
from bs4 import BeautifulSoup
import uuid
from ..utils import (
  enforce_required_props, 
  split_props, 
  parse_prop, 
  fetch_prop,
  create_chained_function,
  get_prop_value,
  resolve_variable,
  resolve_prop_variables,
  convert_props_to_html,
  amend_html_props_to_tag,
  get_prop_from_tag
)

register = template.Library()

@register.tag('file_input')
def file_input(parser, token):
  props = token.split_contents()[1:]

  if not fetch_prop('form', props):
    enforce_required_props(['label'], props)

  props = create_chained_function('onchange', 'handleFileInputChange(event);', props)
  props = create_chained_function('ondragenter', 'handleFileInputDragEnter(event);', props)
  props = create_chained_function('ondragleave', 'handleFileInputDragLeave(event);', props)
  props = create_chained_function('ondrop', 'handleFileInputDrop(event);', props)

  picked_props, file_input_props = split_props(['label', 'accept', 'id', 'input', 'name' 'form'], props)
  
  label = get_prop_value('label', picked_props, None)
  accept = get_prop_value('accept', picked_props, None)
  file_input_id = get_prop_value('id', picked_props, str(uuid.uuid4().int))
  alt_input = get_prop_value('input', picked_props, None)
  alt_form = get_prop_value('form', picked_props, None)
  name = get_prop_value('name', picked_props, None)


  return FileInput(label, accept, file_input_id, alt_input, alt_form, name, file_input_props)


class FileInput(Node):
  def __init__(self, label, accept, file_input_id, alt_input, alt_form, name, file_input_props):
    self.label = label
    self.accept = accept
    self.file_input_id = file_input_id
    self.alt_input = alt_input
    self.alt_form = alt_form
    self.file_input_props = file_input_props
    self.name = name

  def render(self, context):
    self.file_input_props = resolve_prop_variables(self.file_input_props, context)

    alt_input = resolve_variable(self.alt_input, context)
    if alt_input:
      self.file_input_id = alt_input.id_for_label

    file_input_html = get_template("file_input/index.html")
    context.update({
      'label': resolve_variable(self.label, context),
      'accept': resolve_variable(self.accept, context),
      'id': resolve_variable(self.file_input_id, context)
    })

    return self.process_markup(file_input_html.render(context))

  def process_markup(self, markup):
    html_props = convert_props_to_html(self.file_input_props)
    markup = amend_html_props_to_tag(html_props, markup, 'input')
    return markup
