# coding=utf-8
import math

from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.loader import render_to_string

from lifts.models import LiftPart

from django.conf import settings


def index(request):
    return render(request, 'main.html', RequestContext(request))


def add_to_cart(request):
    if request.method == "POST":
        #basket logic
        part_id = int(request.POST["part_id"])
        amount  = int(request.POST["amount"])
        if not request.session.has_key('cart'):
            # инициализация корзины
            request.session['cart'] = {}
        request.session['cart'][part_id] = amount

    return redirect('/cart/')


def cart(request):
    if not request.session.has_key('cart'):
        request.session['cart'] = {}

    part_ids = request.session['cart'].keys()
    parts = LiftPart.objects.filter(id__in=part_ids)
    for part in parts:
        setattr(part, 'amount', request.session['cart'][str(part.id)])

    return render(request, 'cart.html', context=RequestContext(request, {
        'parts': parts,
    }))

def parts(request, kind):
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


def order(request):
    if request.method == 'POST':
        fio = request.POST['fio']
        email = request.POST['email']
        phone = request.POST['phone']
        attachment = request.FILES.get('attachment')
        comment = request.POST['comment']

        part_ids = []
        for part_id, amount in request.session['cart'].items():
            if int(amount) > 0:
                part_ids.append(part_id)

        parts = LiftPart.objects.filter(id__in=part_ids)
        for part in parts:
            setattr(part, 'amount', request.session['cart'][str(part.id)])

        template = render_to_string(
            'order.html',
            {
                'fio': fio,
                'email': email,
                'phone': phone,
                'comment': comment,
                'parts': parts,
                'attachment': attachment,
            }
        )

        mail = EmailMessage(u'Новый заказ', template, [email], settings.ORDER_EMAILS)
        mail.attach(attachment.name, attachment.read(), attachment.content_type)
        mail.send()
        request.session.clear()

    return render(
        request,
        template_name='order_success.html',
    )
