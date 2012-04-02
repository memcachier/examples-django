from django.shortcuts import render_to_response
from django.http import HttpResponse

def home(request):
  return render_to_response('index.html', {})

def compute(request):
  try:
    a = int(request.GET["a"])
    b = int(request.GET["b"])
    op = request.GET["op"]
  
    if op == "plus":
      result = a + b
    else:
      result = a - b
  
    return HttpResponse(result)
  except:
    return HttpResponse("give us two values to add or subtract")