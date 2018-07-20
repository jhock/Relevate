from django import template
from django.template.loader import get_template
from django.template.base import Node
from ..utils import (
  enforce_required_props,
  get_prop_value,
  resolve_variable,
)

register = template.Library()

@register.tag('tag')
def tag(parser, token):
  props = token.split_contents()[1:]

  enforce_required_props(['title'], props)

  title = get_prop_value('title', props, None)
  href = get_prop_value('href', props, '#')
  margin = get_prop_value('margin', props, '0')  

  return Tag(title, href, margin)


class Tag(Node):
  def __init__(self, title, href, margin):
    self.title = title
    self.href = href
    self.margin = margin

  def render(self, context):
    tag_html = get_template("tag/index.html")

    context.update({
      'title': resolve_variable(self.title, context),
      'href': resolve_variable(self.href, context),
      'margin': resolve_variable(self.margin, context)
    })

    return tag_html.render(context)
