from django.template.base import TemplateSyntaxError

def parse_tag(parser, token, closetag):
  nodelist = parser.parse((closetag,))
  arguments = token.split_contents()

  try:
    context_extras = [t.split("=")[1].strip('"') for t in arguments[2:]]
  except IndexError:
    raise TemplateSyntaxError("error parsing arguments")
  parser.delete_first_token()

  return nodelist, context_extras

def enforce_required_props(required_props, props):
  missing_props = []
  for required_prop in required_props:
    if not contains_prop(required_prop, props):
      missing_props.append(required_prop)

  if len(missing_props) > 0:
    raise TemplateSyntaxError("The following props are required: " + ", ".join(str(p) for p in missing_props))
  return

def contains_prop(query, props):
  for prop in props:
    key, value = parse_prop(prop)
    if key == query:
      return True
  return False

def prop_index(query, props):
  for prop in props:
    key, value = parse_prop(prop)
    if key == query:
      return props.index(prop)
  return -1

def parse_prop(prop):
  prop_arr = prop.split('=')
  if len(prop_arr) == 1:
    return prop_arr[0], None
  else:
    return prop_arr[0], prop_arr[1]

def fetch_prop(query, props):
  query_index = prop_index(query, props)
  if query_index > -1:
    return props[query_index]
  else:
    return None
    

# Function splitting the props. Will return an array of
# the requested props, and also a second array containing
# the rest
def split_props(requested_props, props):
  matches = []
  rest = []
  for prop in props:
    if parse_prop(prop)[0] in requested_props:
      matches.append(prop)
    else:
      rest.append(prop)
  return matches, rest

def create_chained_function(query, function_to_chain, props):
  index = prop_index(query, props)
  if index > -1:
    if props[index][:-1] != ';':
      props[index] = props[index] + ';'
    props[index] = props[index] + function_to_chain
  else:
    props.append(query + '=' + function_to_chain)
  return props