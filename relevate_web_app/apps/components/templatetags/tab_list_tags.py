from django import template
from django.template.loader import get_template
from django.template.base import Node, Token
from django.utils.html import format_html
from ..utils import (
  parse_tag,
  enforce_required_props,
  get_prop_value,
  resolve_variable,
)
import uuid
import pdb

register = template.Library()

@register.tag('tab_list')
def tab_list(parser, token):
  children, _ = parse_tag(parser, token, 'end_tab_list')
  
  tab_panels = []
  for child in children:
    if child.token and child.token.token_type == 2:
      tab_panels.append(child)

  return TabList(tab_panels)

@register.tag('tab_panel')
def tab_panel(parser, token):
  children, _ = parse_tag(parser, token, 'end_tab_panel')
  props = token.split_contents()[1:]

  enforce_required_props(['title'], props)
  title = get_prop_value('title', props, None)

  return TabPanel(children, title, str(uuid.uuid4().int)[:10])

class TabList(Node):
  def __init__(self, tab_panels):
    self.tab_panels = tab_panels

  def render(self, context):
    tabs = []
    panel_markup = ''
    for i in range(0, len(self.tab_panels)):
      tab_panel = self.tab_panels[i]
      tab_id = str(uuid.uuid4().int)[:10]
      tabs.append(Tab(tab_panel.title, tab_id, tab_panel.panel_id))
      context.update({
        'active': i == 0,
        'tab_id': tab_id
      })
      panel_markup = panel_markup + tab_panel.render(context)

    tab_markup = ''
    for i in range(0, len(tabs)):
      tab = tabs[i]
      context.update({
        'active': i == 0
      })
      tab_markup = tab_markup + tab.render(context)

    markup = tab_markup + panel_markup

    context.update({
      'tab_panels': format_html(markup)
    })

    tab_list_html = get_template('tab_list/index.html')
    return tab_list_html.render(context)

class Tab(Node):
  def __init__(self, title, tab_id, panel_id):
    self.title = title
    self.tab_id = tab_id
    self.panel_id = panel_id

  def render(self, context):
    tab_html = get_template('tab_list/tab/index.html')

    context.update({
      'title': resolve_variable(self.title, context),
      'tab_id': self.tab_id,
      'panel_id': self.panel_id
    })

    return tab_html.render(context)

class TabPanel(Node):
  def __init__(self, children, title, panel_id):
    self.children = children
    self.title = title
    self.panel_id = panel_id

  def render(self, context):
    tab_panel_html = get_template('tab_list/tab_panel/index.html')

    context.update({
      'children': self.children.render(context),
      'panel_id': self.panel_id
    })

    return tab_panel_html.render(context)
