from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.cache import cache

def home(request):
  return render_to_response('index.html', {})

def compute(request):
  try:
    a = int(request.GET["a"])
    b = int(request.GET["b"])
    op = request.GET["op"]
    expr = "%d%s%d" % (a, op, b)
  
    in_cache = cache.get(expr)
    if in_cache:
      result = in_cache
      message = "hit"
    else:
      if op == "plus":
        result = str(a + b)
      else:
        result = str(a - b)
      message = "miss"
      cache.set(expr, result)

    return HttpResponse("%s<br />cache: %s" % (result, message))
  except:
    return HttpResponse("give us two values to add or subtract")