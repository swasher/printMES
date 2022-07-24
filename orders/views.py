# coding: utf-8

from io import BytesIO
from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse
from django.template import RequestContext
from orders.models import Order, PrintSheet, Operation, Detal
from orders.forms import NewOrderForm
# from .reporting_reportlab import PrintOrder
from .reporting_borb import PrintOrder
# from reporting import printpdf
from django.http import FileResponse, Http404


def create_new_order(request):
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            pass  # Обрабатываем данные, производим запись в базу
    else:
        # Показываем пустую форму
        form = NewOrderForm()
    return render(request, 'new_order.html', {'form': form})


def orders(request):
    table = Order.objects.all()
    return render(request, 'orders.html', {'table': table})


# DEPRECATED
# def print_html_order(request, orderid):
#     context = RequestContext(request)
#     try:
#         order = Order.objects.get(pk=orderid)
#     except order.DoesNotExist:
#         raise Http404
#
#     return render_to_response('order_print.html', {'order': order})


def copy_order(request, orderid):
    from django.db.models import Max
    from copy import deepcopy

    try:
        order = Order.objects.get(pk=orderid)
    except order.DoesNotExist:
        raise Http404

    # Дублируем новый объект ЗАКАЗ
    new_order = deepcopy(order)
    new_order.id = None
    last_number = Order.objects.all().aggregate(Max('order'))['order__max']
    new_order.order = int(last_number) + 1
    new_order.save()

    # Итерация по печатным листам, каждый дублируем
    printsheets = PrintSheet.objects.filter(order_id=order.id)
    for printsheet in printsheets:
        new_printsheet = deepcopy(printsheet)
        new_printsheet.id = None
        new_printsheet.order_id = new_order.id
        new_printsheet.save()

        # Итерация по технологическим операциям, которые ИМЕЮТ ВЛАДЕЛЬЦА-ПЕЧАТНЫЙ ЛИСТ, каждую дублируем
        operations = Operation.objects.filter(order_id=order.id).filter(printsheet_id=printsheet.id)
        for operation in operations:
            new_operation = deepcopy(operation)
            new_operation.id = None
            new_operation.printsheet_id = new_printsheet.id
            new_operation.order_id = new_order.id
            new_operation.save()

        # Далее итерация по Деталям, они все имеют предка-владельца Печатный лист
        detals = Detal.objects.filter(printsheet_id=printsheet.id)
        for detal in detals:
            new_detal = deepcopy(detal)
            new_detal.id = None
            new_detal.printsheet_id = new_printsheet.id
            new_detal.save()

    # Итерация по технологическим операциям, которые НЕ ИМЕЮТ ПРЕДКА-ПЕЧАТНОГО ЛИСТА, каждую дублируем
    operations = Operation.objects.filter(order_id=order.id).filter(printsheet_id=None)
    for operation in operations:
        new_operation = deepcopy(operation)
        new_operation.id = None
        new_operation.order_id = new_order.id
        new_operation.save()

    return redirect('/')


def print_pdf_order_reportlab_version(request, orderid):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="My Users.pdf"'

    buffer = BytesIO()
    report = PrintOrder(buffer, orderid)
    pdf = report.printpdf()

    response.write(pdf)
    return pdf


def print_pdf_order(request, orderid):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="output.pdf"'


    # via reportlab
    # buffer = BytesIO()
    # report = PrintOrder(buffer, orderid)
    # pdf = report.printpdf()

    order = Order.objects.get(pk=orderid)
    # via borb
    report = PrintOrder(order)
    pdf = report.printpdf()

    try:
        return FileResponse(open('output.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
