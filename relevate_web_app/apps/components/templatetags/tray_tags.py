from django import template
from django.template.loader import get_template
from django.template.base import Node, Token
from django.utils.html import format_html
from bs4 import BeautifulSoup
from ..utils import (
  parse_tag,
  enforce_required_props,
  get_prop_value,
  resolve_variable,
)
import uuid

import pdb

register = template.Library()

@register.tag('tray')
def tray(parser, token):
  children, _ = parse_tag(parser, token, 'end_tray')
  props = token.split_contents()[1:]

  enforce_required_props(['label', 'closeButtonLabel'], props)
  label = get_prop_value('label', props, None)
  closeButtonLabel = get_prop_value('closeButtonLabel', props, None)
  placement = get_prop_value('placement', props, 'start')
  
  tray_children = []
  for child in children:
    if child.token and child.token.token_type == 2:
      tray_children.append(child)

  return Tray(tray_children, label, closeButtonLabel, placement)

@register.tag('tray_trigger')
def tray_trigger(parser, token):
  children, _ = parse_tag(parser, token, 'end_tray_trigger')
  return TrayTrigger(children)

@register.tag('tray_content')
def tray_content(parser, token):
  children, _ = parse_tag(parser, token, 'end_tray_content')
  return TrayContent(children)

class Tray(Node):
  def __init__(self, children, label, closeButtonLabel, placement):
    self.children = children
    self.label = label
    self.closeButtonLabel = closeButtonLabel
    self.placement = placement

  def render(self, context):
    tray_markup = ''
    for i in range(0, len(self.children)):
      child = self.children[i]
      if child.type == 'tray_content':
        context.update({
          'tray_label': resolve_variable(self.label, context),
          'tray_close_button_label': resolve_variable(self.closeButtonLabel, context),
          'tray_placement': self.placement
        })

      tray_markup = tray_markup + child.render(context)

    context.update({
      'tray_children': format_html(tray_markup)
    })

    tray_html = get_template('tray/index.html')
    return tray_html.render(context)

class TrayTrigger(Node):
  def __init__(self, children):
    self.type = 'tray_trigger'
    self.children = children

  def render(self, context):
    tab_html = get_template('tray/tray_trigger/index.html')

    button = self.children.render(context)
    soup = BeautifulSoup(button, 'html.parser')
    soup.find()['onclick'] = 'handleTrayTriggerClick(event)'

    context.update({
      'tray_trigger_children': format_html(str(soup))
    })

    return tab_html.render(context)

class TrayContent(Node):
  def __init__(self, children):
    self.type = 'tray_content'
    self.children = children

  def render(self, context):
    tray_content_html = get_template('tray/tray_content/index.html')

    context.update({
      'tray_content_children': self.children.render(context)
    })

    return tray_content_html.render(context)
