from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
from bs4 import BeautifulSoup
import uuid, re
from ..utils import (
  enforce_required_props, 
  split_props, 
  parse_prop,  
  fetch_prop,
  get_prop_value,
  resolve_variable,
  resolve_prop_variables,
  convert_props_to_html,
  amend_html_props_to_tag,
  get_prop_from_tag
)

import pdb

register = template.Library()

@register.tag('checkbox')
def checkbox(parser, token):
  props = token.split_contents()[1:]

  if not fetch_prop('form', props):
    enforce_required_props(['label'], props)

  picked_props, checkbox_props = split_props(['label', 'id', 'input', 'form', 'name'], props)
  
  label = get_prop_value('label', picked_props, None)
  checkbox_id = get_prop_value('id', picked_props, str(uuid.uuid4().int))
  alt_input = get_prop_value('input', picked_props, None)
  alt_form = get_prop_value('form', picked_props, None)
  checkbox_name = get_prop_value('name', picked_props, None)

  return Checkbox(label, checkbox_id, alt_input, alt_form, checkbox_name, checkbox_props)


class Checkbox(Node):
  def __init__(self, label, checkbox_id, alt_input, alt_form, checkbox_name,checkbox_props):
    self.label = label
    self.checkbox_id = checkbox_id,
    self.alt_input = alt_input,
    self.alt_form = alt_form,
    self.checkbox_name = checkbox_name,
    self.checkbox_props = checkbox_props

  def render(self, context):
    self.checkbox_props = resolve_prop_variables(self.checkbox_props, context)

    alt_input = resolve_variable(self.alt_input, context)
    if alt_input:
      try:
        soup = BeautifulSoup(alt_input.render(), 'html.parser')
        self.parse_id(soup)
      except:
        self.checkbox_id = alt_input.id_for_label

    alt_form = resolve_variable(self.alt_form, context)
    if alt_form:
      try:
        soup = BeautifulSoup(alt_form.render(), 'html.parser')
        self.parse_id(soup)
        self.parse_label(soup)
      except:
        self.checkbox_id = alt_input.id_for_label
        self.label = alt_input.label


    checkbox_html = get_template("checkbox/index.html")
    context.update({
      'label': resolve_variable(self.label, context),
      'id': resolve_variable(self.checkbox_id, context),
      'name': resolve_variable(self.checkbox_name, context),
    })

    return checkbox_html.render(context)

  def parse_id(self, soup):
    alt_id = soup.find('input').attrs['id']
    if alt_id:
      self.checkbox_id = alt_id

  def parse_label(self, soup):
    label = soup.find('label').getText()
    if label:
      self.label = label
