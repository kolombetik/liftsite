# coding=utf-8
import math
from django.db.models import Q
from django.shortcuts import render
from django.template import RequestContext

from lifts.models import LiftPart


def index(request):
    return render(request, 'main.html', RequestContext(request))


def add_to_cart (part_id, amount, session):
    if 'cart' not in session:
        # инициализация корзины
        session['cart'] = {}
    session['cart'][part_id] = amount


def parts(request, kind):
    if request.method == "POST":
        #basket logic
        part_id = request.POST["part_id"]
        amount  = request.POST["amount"]
        add_to_cart (part_id, amount, request.session)


    page=request.GET.get("page", 1)
    limit=20
    offset=int(page)*limit - limit
    max_offset=offset+limit
    parts=LiftPart.objects.filter(kind=kind).order_by("name")[offset:max_offset]
    count=LiftPart.objects.filter(kind=kind).count()
    total_pages=math.ceil(float(count)/limit)
    return render(request, 'parts.html', context=RequestContext(request, {
        'parts': parts,
        'total_pages': range(1,int(total_pages)+1),
        'last_page': int(total_pages),
        'kind': kind,
        'current_page': int(page),
    }))

def contacts(request):
    return render(request, 'contacts.html')


def part_page(request, part_id):
    part = LiftPart.objects.get(id=part_id)

    return render(request, 'part.html', context=RequestContext(request, {
        'part': part,
    }))


def search(request):
    search_term = request.GET.get('search_term', '')
    lift_parts = LiftPart.objects.filter(
               Q(name__icontains=search_term) |
        Q(description__icontains=search_term) |
        Q(full_description__icontains=search_term)
    )

    return render(request, 'parts.html', context=RequestContext(request, {
        'parts': lift_parts,
    }))