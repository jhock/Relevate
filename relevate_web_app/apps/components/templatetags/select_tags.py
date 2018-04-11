from django import template
from django.template.loader import get_template
from django.template.base import Node, Token
from bs4 import BeautifulSoup
import uuid
from ..utils import (
  parse_tag, 
  enforce_required_props, 
  split_props, 
  get_prop_value,
  resolve_variable,
  resolve_prop_variables,
  convert_props_to_html,
  amend_html_props_to_tag,
)

register = template.Library()

@register.tag('select')
def text_input(parser, token):
  props = token.split_contents()[1:]
  enforce_required_props(['label'], props)

  picked_props, input_props = split_props(['id', 'input', 'label', 'editable', 'options'], props)
  input_id = get_prop_value('id', picked_props, str(uuid.uuid4().int))
  alt_input = get_prop_value('input', picked_props, None)
  label = get_prop_value('label', picked_props, None)
  editable = get_prop_value('editable', picked_props, 'False')
  options = get_prop_value('options', picked_props, None)

  children = None
  if not options:
    children, _ = parse_tag(parser, token, 'end_select')

  return Select(children, label, input_id, alt_input, input_props, options, editable)


class Select(Node):
  def __init__(self, children, label, input_id, alt_input, input_props, options, editable):
    self.children = children
    self.label = label
    self.input_id = input_id
    self.alt_input = alt_input
    self.input_props = input_props
    self.options = options
    self.editable = editable

  def render(self, context):
    if self.editable == 'False':
      self.input_props.append('readonly')

    input_props = resolve_prop_variables(self.input_props, context)
    options = resolve_variable(self.options, context)

    if self.children:
      child_options = self.parse_options(self.children.render(context))
    else:
      child_options = ''

    select_html = get_template("select/index.html")
    context.update({
      'label': resolve_variable(self.label, context),
      'id': resolve_variable(self.input_id, context),
      'alt_input': resolve_variable(self.alt_input, context),
      'options': options or child_options,
      'options_id': str(uuid.uuid4())
    })
    markup = select_html.render(context)

    html_props = convert_props_to_html(input_props)
    markup = amend_html_props_to_tag(html_props, markup, 'input')
    return markup

  def parse_options(self, html_options):
    options = []
    soup = BeautifulSoup(html_options, 'html.parser')
    for option in soup.find_all('option'):
      options.append(option.get_text())

    return options
