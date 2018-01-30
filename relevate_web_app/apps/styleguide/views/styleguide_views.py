from django.shortcuts import render
from django.views.generic import View
from ..examples import examplesData
import string

class StyleguideView(View):
  def get(self, request):
    for data in examplesData:
      if data.rawName in request.path:
        return render(request, 'examples/' + data.rawName + '.html', {'examplesData': examplesData, 'displayName': data.displayName, 'cssFilePath': data.cssFilePath, 'jsFilePath':data.jsFilePath})

    return render(request, 'index.html', {'examplesData': examplesData})
