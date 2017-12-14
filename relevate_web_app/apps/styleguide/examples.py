from os import listdir
from os.path import dirname, join, splitext
from collections import namedtuple
import string
import pdb

ExampleData = namedtuple('ExampleData', ['rawName', 'displayName', 'cssFilePath', 'jsFilePath'])

examplesDir = 'templates/examples'
examplesDir = join(dirname(__file__), examplesDir)
exampleFiles = listdir(examplesDir)

# Raw names only
examples = []
for file in exampleFiles:
  examples.append(splitext(file)[0])

# Raw names and display names
examplesData = []
for example in examples:
  displayName = example.replace('-', ' ')
  displayName = example.replace('_', ' ')
  displayName = string.capwords(displayName)

  appName = 'relevate_web_app'

  componentCssDir = 'static/scss/components'
  componentCssDirAbs = join(dirname(dirname(dirname(__file__))), componentCssDir)
  componentCssFiles = listdir(componentCssDirAbs)
  cssFileName = '_' + example.replace('_', '-') + '.scss'
  cssFilePath = appName + '/' + componentCssDir + '/' + cssFileName

  if cssFileName not in componentCssFiles:
    cssFilePath = None

  componentJsDir = 'static/js/components'
  componentJsDirAbs = join(dirname(dirname(dirname(__file__))), componentJsDir)
  componentJsFiles = listdir(componentJsDirAbs)
  jsFileName = example.replace('_', '-') + '.js'
  jsFilePath = appName + '/' + componentJsDir + '/' + jsFileName

  if jsFileName not in componentJsFiles:
    jsFilePath = None

  examplesData.append(ExampleData(example, displayName, cssFilePath, jsFilePath))
  