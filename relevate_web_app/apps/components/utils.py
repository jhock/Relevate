def parse_tag(parser, token, closetag):
  nodelist = parser.parse((closetag,))
  arguments = token.split_contents()

  try:
    context_extras = [t.split("=")[1].strip('"') for t in arguments[2:]]
  except IndexError:
    raise TemplateSyntaxError("error parsing arguments")
  parser.delete_first_token()

  return nodelist, context_extras