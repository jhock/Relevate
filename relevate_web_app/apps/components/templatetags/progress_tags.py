from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
from django.utils.html import format_html
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
import pdb

register = template.Library()

@register.tag('progress')
def progress(parser, token):
  children, _ = parse_tag(parser, token, 'end_progress')
  
  progress_items = []
  for child in children:
    if child.token and child.token.token_type == 2:
      progress_items.append(child)

  return Progress(progress_items)

@register.tag('progress_item')
def progress_item(parser, token):
  children, _ = parse_tag(parser, token, 'end_progress_item')
  props = token.split_contents()[1:]
  status = get_prop_value('status', props, 'initial')
  return ProgressItem(children, status)

class Progress(Node):
  def __init__(self, progress_items):
    self.progress_items = progress_items

  def render(self, context):
    markup = ''
    for i in range(0, len(self.progress_items)):
      progress_item = self.progress_items[i]
      context.update({
        'position': ' | ' + str(i + 1) + ' of ' + str(len(self.progress_items))
      })
      markup = markup + progress_item.render(context)

    progress_html = get_template("progress/index.html")
    context.update({
      'children': format_html(markup)
    })
    return progress_html.render(context)

class ProgressItem(Node):
  def __init__(self, children, status):
    self.children = children
    self.status = status

  def render(self, context):
    progress_item_html = get_template("progress/progress_item/index.html")
    context.update({
      'children': self.children.render(context),
      'status': resolve_variable(self.status, context)
    })
    return progress_item_html.render(context)