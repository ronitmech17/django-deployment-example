from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import AccessRecord,Topic,Webpage

# Create your views here.

def index(request):
    #return HttpResponse("Hello world!!")
    webPages_list = Webpage.objects.order_by('topic')
    my_dict = {'webPages':webPages_list}
    return render(request,'first_app/index.html',context=my_dict)
