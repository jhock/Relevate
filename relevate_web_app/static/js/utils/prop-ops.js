function omitProps (props, propsToOmit) {
  var propKeys = Object.keys(props)
  var omitKeys = Object.keys(propsToOmit)
  var result = {}

  for (var i = 0; i < propKeys.length; i++) {
    var propKey = propKeys[i]
    if (omitKeys.indexOf(propKey) === -1) {
      result[propKey] = props[propKey]
    }
  }
  return result
}

function parseExistingProps (el) {
  var attributes = el.getAttributeNames()
  var result = {}

  for (var i = 0; i < attributes.length; i++) {
    var attribute = attributes[i]
    if (attribute === 'class') {
      result['className'] = el.getAttribute(attribute)
    } else {
      result[convertHyphenToCamelCase(attribute)] = el.getAttribute(attribute)
    }
  }
  return result
}

function mergeProps (props, existingProps) {
  var propKeys = Object.keys(props)
  var existingPropKeys = Object.keys(existingProps)
  var result = {}

  var keys = mergeArrays(propKeys, existingPropKeys)

  for (var i = 0; i < keys.length; i++) {
    var key = keys[i]

    if (key.indexOf('on') === 0) {
      if (props[key] && existingProps[key]) {
        var handler = existingProps[key].trim()
        if (handler[handler.length - 1] !== ';') {
          handler += ';'
        }
        handler += props[key]
        result[key] = handler
      } else {
        result[key] = existingProps[key] || props[key]
      }
    } else {
      result[key] = existingProps[key] || props[key]
    }
  }

  return result
}

function removeAttributes (el) {
  while(el.attributes.length > 0) {
    el.removeAttribute(el.attributes[0].name)
  }
  return el
}

function ammendPropsToElement (props, el) {
  var existingProps = parseExistingProps(el)
  var mergedProps = mergeProps(props, existingProps)

  propKeys = Object.keys(mergedProps)

  el = removeAttributes(el)
  for (var i = 0; i < propKeys.length; i++) {
    var propKey = propKeys[i]
    if (propKey === 'className') {
      el.setAttribute('class', mergedProps[propKey])
    } else {
      el.setAttribute(convertCamelCaseToHyphen(propKey), mergedProps[propKey])
    }
  }
}

function mergeArrays(arr1, arr2) {
  for (var i = 0; i < arr1.length; i++) {
    if (arr2.indexOf(arr1[i]) === -1) {
      arr2.push(arr1[i])
    }
  }
  return arr2
}

function convertCamelCaseToHyphen (str) {
  return str.replace( /([a-z])([A-Z])/g, '$1-$2' ).toLowerCase();
}

function convertHyphenToCamelCase(str) {
  return str.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase() })
}

function testFunc () {
  console.log('foo bar baz')
}