from django import template
from django.template.loader import get_template
from django.template.base import Node, Token, TemplateSyntaxError
from ..utils import parse_tag

register = template.Library()


@register.tag('dropdown_menu')
def dropdown_menu(parser, token):
  nodelist, _ = parse_tag(parser, token, 'end_dropdown_menu')
  return DropdownMenu(nodelist)


@register.tag('dm_trigger')
def dropdown_menu_trigger(parser, token):
  nodelist, context_extras = parse_tag(parser, token, 'end_dm_trigger')
  return DropdownMenuTrigger(nodelist, *context_extras)


@register.tag('dm_content')
def dropdown_menu_trigger(parser, token):
  nodelist, context_extras = parse_tag(parser, token, 'end_dm_content')
  return DropdownMenuContent(nodelist, *context_extras)


@register.tag('dm_item')
def dropdown_menu_item(parser, token):
  nodelist, context_extras = parse_tag(parser, token, 'end_dm_item')
  return DropdownMenuItem(nodelist, *context_extras)


@register.tag('dm_label')
def dropdown_menu_label(parser, token):
  nodelist, context_extras = parse_tag(parser, token, 'end_dm_label')
  return DropdownMenuLabel(nodelist, *context_extras)


@register.inclusion_tag('dropdown_menu/dropdown_menu_separator/index.html')
def dm_separator():
  return {}


class DropdownMenu(Node):
  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    dropdown_menu_html = get_template("dropdown_menu/index.html")
    context.update({
      'content' : self.nodelist.render(context),
    })
    return dropdown_menu_html.render(context)


class DropdownMenuTrigger(Node):
  def __init__(self, nodelist, id, className, withArrow = 'False'):
    self.nodelist = nodelist
    self.id = id
    self.className = className
    self.withArrow = withArrow if withArrow == 'True' else None 

  def render(self, context):
    dropdown_menu_trigger_html = get_template("dropdown_menu/dropdown_menu_trigger/index.html")
    context.update({
      'label' : self.nodelist.render(context),
      'id': self.id,
      'className': self.className,
      'withArrow': self.withArrow
    })
    return dropdown_menu_trigger_html.render(context)


class DropdownMenuContent(Node):
  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    dropdown_menu_content_html = get_template("dropdown_menu/dropdown_menu_content/index.html")
    context.update({
      'content' : self.nodelist.render(context),
    })
    return dropdown_menu_content_html.render(context)


class DropdownMenuItem(Node):
  def __init__(self, nodelist, href):
    self.nodelist = nodelist
    self.href = href

  def render(self, context):
    dropdown_menu_item_html = get_template("dropdown_menu/dropdown_menu_item/index.html")
    context.update({
      'content' : self.nodelist.render(context),
      'href' : self.href
    })
    return dropdown_menu_item_html.render(context)


class DropdownMenuLabel(Node):
  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    dropdown_menu_label_html = get_template("dropdown_menu/dropdown_menu_label/index.html")
    context.update({
      'content' : self.nodelist.render(context),
    })
    return dropdown_menu_label_html.render(context)


class DropdownMenuSeparator(Node):
  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    dropdown_menu_label_html = get_template("dropdown_menu/dropdown_menu_separator/index.html")
    context.update({
      'content' : self.nodelist.render(context),
    })
    return dropdown_menu_label_html.render(context)