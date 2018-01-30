from django import template
from django.template.loader import get_template
from django.template.base import Node, TemplateSyntaxError

register = template.Library()

class Example(Node):
  def __init__(self, nodelist, example, heading, caption, codeOnly='False'):
    self.nodelist = nodelist
    self.caption = caption
    self.heading = heading
    self.example = example
    self.codeOnly = codeOnly if codeOnly == 'True' else None

  def render(self, context):
    example_html = get_template("example.html")
    context.update({
      'caption' : self.caption,
      'heading' : self.heading,
      'example' : self.example,
      'rows' : self.example.count('\n'),
      'codeOnly': self.codeOnly,
      'markup' : self.nodelist.render(context),
    })
    return example_html.render(context)

@register.tag('example')
def example(parser, token):
  closetag = 'end_example'
  example = parse_example(parser, closetag)

  nodelist = parser.parse((closetag,))
  props = token.split_contents()
  context_extras = [t.split("=")[1].strip('"') for t in props[2:]]
  parser.delete_first_token()
  return Example(nodelist, example, *context_extras)

def parse_example(parser, closetag):
  tokens = parser.tokens
  example = ''
  for token in tokens:
    if token.contents == closetag:
      break
    if (token.token_type == 2):
      example = example + '{% ' + token.contents + ' %}'
    else:
      example = example + token.contents
  return example
