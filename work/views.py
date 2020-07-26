from django.shortcuts import render
from .models import Loading, UnLoading, StorageResult
from storage.models import StorageCatalog
from django.http import HttpResponse, HttpResponseRedirect
import re, json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.wkt import loads
from django.urls import reverse


def index(request):
    loadings = Loading.objects.all()
    results = StorageResult.objects.all()
    return render(request, 'work/index.html', {'loadings': loadings, 'results': results})


def unload(request):
    coords = request.GET['coords']
    match = re.fullmatch(r'^([0-9]*[.,][0-9]*|[0-9]*)+\s([0-9]*[.,][0-9]*|[0-9]*)$', coords)
    if match:
        storage = StorageCatalog.objects.get(id=1)
        coords = coords.replace(',', '.')
        point_coords = loads('POINT (' + coords + ')')
        point = Point(point_coords)
        polygon = Polygon(loads(storage.coords))
        is_contains = polygon.contains(point)
        if is_contains:
            loading = Loading.objects.get(id=request.GET['number'])
            UnLoading.objects.create(loading=loading, storage=storage)
            data = json.dumps({'text_response': ''})
        else:
            data = json.dumps({'text_response': 'Координаты разгрузки не входят в координаты склада'})
    else:
        data = json.dumps({'text_response': 'Неверный формат ввода. Дожно быть 2 числа, разделенных пробелом.'})
    return HttpResponse(data)
