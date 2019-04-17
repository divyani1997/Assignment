from django.http import JsonResponse
import urllib.request
from django.core.cache import cache
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', 300)

# Create your views here.

def index(request):
    data = {"data": "pong"}
    return JsonResponse(data)

def detail(request):
    nocache=request.GET.get('nocache',0)
    scode=request.GET.get('scode','')
    if nocache==1 and cache.get('scode')==scode:
        viewdata=cache.get('viewdata')
        cache.delete('scode')
        cache.delete('viewdata')
        return JsonResponse(viewdata)
    url='https://tgftp.nws.noaa.gov/data/observations/metar/stations/'
    urlnew=url+scode+'.TXT'
    with urllib.request.urlopen(urlnew) as url1:
      data = url1.read()
    tempdata=data.decode().replace('\n',' ').split(' ')
    temperature=tempdata[8].split('/')[0]
    finaltemperature=''
    fahreneit=''
    if temperature.startswith('M'):
        finaltemperature='-'+ temperature[1:] + 'C '
        fahreneit=int(temperature[1:])
    else:
        finaltemperature=temperature[0:] + 'C '
        fahreneit=int(temperature[0:])
    f=fahreneit*1.8+32
    viewdata={'data':{'station': scode, 'last_observation': tempdata[0]+' at '+ tempdata[1]+' GMT', 'temperature': finaltemperature + '(' + str(f) +'F)', 'wind': tempdata[5]}}
    cache.set('scode', scode)
    cache.set('viewdata', viewdata)
    return JsonResponse(viewdata)
