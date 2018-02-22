from django import template
from django.template.base import TemplateSyntaxError
import re

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

def get_prop_value(query, props, default):
  prop = fetch_prop(query, props)
  if prop:
    return parse_prop(prop)[1].replace('\"', '')
  else:
    return default
    

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
    close_str = props[index][-1:]
    function_prop = props[index][:-1]
    if function_prop[:-1] != ';':
      function_prop = function_prop + ';'
    props[index] = function_prop + function_to_chain + close_str
  else:
    props.append(query + '=' + function_to_chain)
  return props

def resolve_variable(prop_value, context):
  if not prop_value:
    return None

  if type(prop_value) is list or type(prop_value) is tuple:
    prop_value = prop_value[0]
    if prop_value is None:
      return None

  variable = template.Variable(prop_value)
  try:
    resolved = variable.resolve(context)
    return resolved
  except template.VariableDoesNotExist:
    return prop_value

def resolve_prop_variables(props, context):
  for i in range(0, len(props)):
    parsed = parse_prop(props[i])
    if parsed[1] is not None:
      props[i] = parsed[0] + '=' + resolve_variable(parsed[1], context)
  return props

def convert_props_to_html(props):
  for i in range(0, len(props)):
    parsed = parse_prop(props[i])
    if parsed[1] is not None:
      props[i] = parsed[0] + '=' + '\"' + parsed[1] + '\"'
  return ' '.join(props)

def amend_html_props_to_tag(html_props, markup, tag):
  search_tag = '<' + tag
  idx = markup.find(search_tag) + len(search_tag)
  res = markup[:idx] + ' ' + html_props + ' ' + markup[idx:]
  return res

def get_prop_from_tag(query, markup, tag):
  tag_re = re.search('<' + tag + '.*>', markup)
  if tag_re is not None:
    tag_markup = tag_re.group(0)
    query_re = re.search(query + '=".*?"', tag_markup)
    if query_re is not None:
      prop = query_re.group(0)
      return prop
    else:
      return None
  else:
    return None

def replace_tag(markup, tag, replace):
  open_tag = '<' + tag
  open_idx = markup.find(open_tag) + len(open_tag)
  markup = '<' + replace + markup[open_idx:]

  close_tag = '</' + tag + '>'
  close_idx = markup.find(close_tag) + len(close_tag)
  markup = markup[:close_idx] + '</' + replace + '>'
  return markup
