from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import SotD

def index(request):
    sotd_list = SotD.objects.order_by('-sotd_date')[:5]
    context = {'sotd_list': sotd_list}
    return render(request, 'sotd/index.html', context)

def sotd(request, sotd_id):
    sotd = get_object_or_404(SotD, pk=sotd_id)
    return render(request, 'sotd/sotd.html', {'sotd': sotd})
