from django import template
from django.template.loader import get_template
from django.template.base import Node
from ..utils import (
    split_props,
    get_prop_value,
    resolve_variable,
    resolve_prop_variables
)

register = template.Library()


@register.tag('avatar')
def avatar(parser, token):
    props = token.split_contents()[1:]

    # picked_props = split_props(['name', 'img_source'], props)

    name = get_prop_value('name', props, None)
    src = get_prop_value('src', props, None)

    return Avatar(name, src)


class Avatar(Node):
    def __init__(self, name, src):
        self.name = self.makeInitialsFromName(name)
        self.src = src

    def render(self, context):
        # self.input_props = resolve_prop_variables(self.input_props, context)

        avatar_html = get_template("avatar/index.html")
        context.update({
            'name': resolve_variable(self.name, context),
            'src': resolve_variable(self.src, context)
        })
        return avatar_html.render(context)

    def makeInitialsFromName(self, name):
        name_list = name.split()

        initials = ""
        number_of_initials = 0

        for name in name_list:
            initials += name[0].upper()
            number_of_initials += 1
        if number_of_initials > 3:
            x = len(initials)
            initials = initials[0:x:x-1]
        return initials