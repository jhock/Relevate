from django import template
from django.template.loader import get_template
from django.template.base import Node, Token
from ..utils import (
  enforce_required_props,
  get_prop_value,
  resolve_variable,
)

import pdb

register = template.Library()

@register.tag('avatar')
def avatar(parser, token):
  props = token.split_contents()[1:]

  enforce_required_props(['name'], props)

  src = get_prop_value('src', props, None)
  name = get_prop_value('name', props, None)    

  return Avatar(src, name)


class Avatar(Node):
  def __init__(self, src, name):
    self.src = src
    self.name = name

  def render(self, context):
    name = str(resolve_variable(self.name, context))
    initials = self.parse_initials(name)
    initial_svgs = []
    for initial in initials:
      try:
        initial_svgs.append(get_template("avatar/letter_svgs/" + initial.lower() + ".html").render(context))
      except:
        initial_svgs.append(initial)

    avatar_html = get_template("avatar/index.html")

    context.update({
      'src': resolve_variable(self.src, context),
      'name': name,
      'initials': initial_svgs
    })

    return avatar_html.render(context)

  def parse_initials(self, name):
    if not name:
      return ['']

    name_array = name.split(' ')
    initials = name_array[0][0].upper()

    if len(name_array) > 1:
      initials += name_array[len(name_array) - 1][0].upper()

    return initials
