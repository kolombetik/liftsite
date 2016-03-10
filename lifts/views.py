from django.db.models import Q
from django.shortcuts import render
from django.template import RequestContext

from lifts.models import LiftPart


def index(request):
    return render(request, 'main.html')


def parts(request):
    return render(request, 'parts.html', context=RequestContext(request, {
        'parts': LiftPart.objects.all()
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
        Q(vendor_code__icontains=search_term) |
        Q(name__icontains=search_term) |
        Q(description__icontains=search_term) |
        Q(full_description__icontains=search_term)
    )

    return render(request, 'parts.html', context=RequestContext(request, {
        'parts': lift_parts,
    }))