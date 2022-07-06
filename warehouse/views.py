import os
import logging
import subprocess
from datetime import datetime
from pathlib import PureWindowsPath
from datetime import datetime

from django.conf import settings
from django.db.models import F, Count, Value
from django.http import HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from smb.SMBConnection import SMBConnection
from pdfrw import PdfReader

from core.models import Customer
from .models import Maquette
from .util import smbwalk
from core.util import reduce_image
from core.util import mm

logger = logging.getLogger(__name__)

class CustomerList(ListView):
    # form_class = MyForm
    # initial = {'key': 'value'}
    # template_name = 'customers.html'
    #
    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.initial)
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         return HttpResponseRedirect('/')
    #
    #     return render(request, self.template_name, {'form': form})

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(CustomerList, self).dispatch(request, *args, **kwargs)

    model = Customer
    template_name = 'customer_list.html'

    # Example how add some data to response
    # def get_context_data(self, **kwargs):
    #     context = super(MyCustomersView, self).get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

    def get_queryset(self):
        return Customer.objects.all()


class Maquette_list(ListView):
    model = Maquette
    template_name = 'maquette_list.html'

    def get_queryset(self):
        list = Maquette.objects.filter(customer__pk=self.kwargs['customerpk'])
            #.annotate(mycolumn=Value(F('thumb')[0:5]))
        return list


class Maquette_detail(DetailView):
    model = Maquette
    template_name = 'maquette_detail.html'

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(Maquette_detail, self).dispatch(request, *args, **kwargs)


@login_required()
def scan(request, customerpk):
    """
    Сканирует удаленную (относительно сервера) директорию по самба-пути.
    Для каждого кастомера существует одна конкретная директория - c.unc.
    Находит все pdf файлы, включая поддиректории.
    Для каждого файла делает джипег, сохраняя структуру папок, и складывает получившееся в MEDIA/warehouse/customer/...
    Для каждого созданного джипега создает инстанс в модели Maquette
    :param request: 
    :param customerpk: 
    :return: 
    """
    c = Customer.objects.get(pk=customerpk)

    # удаляем все старые макеты
    Maquette.objects.filter(customer=c).delete()

    unc = bytes(c.unc, "utf-8").decode("unicode_escape")
    p = PureWindowsPath(unc)
    _, server, service_name, *other = p.parts
    top = '/'.join(other)
    # example values:
    # server = 'JOHN'
    # service_name = 'work' - it's share name
    # top = 'cocacola'

    warehouse_path = os.path.join(settings.MEDIA_ROOT, 'warehouse', c.name) # абсолютный путь к хранению созданных джипегов-макетов
    if not os.path.exists(warehouse_path):
        os.makedirs(warehouse_path)


    conn = SMBConnection(username='', password='', my_name='PDFUPLOAD', remote_name=server, use_ntlm_v2 = True)
    assert conn.connect(server, 139)
    walking = smbwalk(conn, service_name, top=top, pattern='*.pdf')

    for i in walking:
        path = i[0]   # УДАЛЕННЫЙ путь от shared folder к файлу, напр. /cocacola/!MAKETS/etiketki/bottle
        pdfobj = i[1] # объект типа smb.base.SharedFile, соотв. удаленному файлу на самбе
        relative_path_jpg = os.path.relpath(path, top) # ЛОКАЛЬНЫЙ Путь, относительный указанного места хранения
                                             # клиентских файлов. Позволяет
                                             # сохранить структуру хранения файлов и папок. Например,
                                             # в c.unc указано, что файлы заказчика хранятся в //SERVER/share/cocacola/!MAKETS
                                             # тогда relpath будет etiketki/bottle (см. переменную path)

        last_write_float = pdfobj.last_write_time # return float
        last_write = datetime.fromtimestamp(last_write_float)

        absolute_path_jpg = os.path.join(warehouse_path, relative_path_jpg)  # ЛОКАЛЬНЫЙ абсолютный путь
        # Нужно убедится, что такой путь существует
        if not os.path.exists(absolute_path_jpg):
            os.makedirs(absolute_path_jpg)

        local_pdf = os.path.join(warehouse_path, relative_path_jpg, pdfobj.filename)

        with open(local_pdf, 'wb') as f:
            logger.debug('='*40)
            fileattr, filesize = conn.retrieveFile(service_name, os.path.join(path, pdfobj.filename), f)
            logger.debug('Retrived {} [{:.2f}Mb]'.format(pdfobj.filename, filesize/1024/1024))

        # Get trim box of first page
        pages = PdfReader(local_pdf, decompress=False).pages
        box = [float(x) for x in pages[0].TrimBox]
        width, height = mm(box[2]-box[0]), mm(box[3]-box[1])
        logger.debug('BOX: {}x{}'.format(width, height))


        #
        # via GHOSTSCRIPT
        #
        output = os.path.join(absolute_path_jpg, pdfobj.filename + '.jpg')
        gs_convert = 'gs -dNOPAUSE -dBATCH -sDEVICE=jpeg -dJPEGQ=80 -r{resolution} -sOutputFile="{output}" "{input}"'.format(resolution='200', input=local_pdf, output=output)
        subprocess.run(gs_convert, shell=True, check=True)

        #
        # via POPPLER
        #
        # poppler = 'pdftoppm -jpeg -r 300 "{input}" "{prefix}"'.format(input=localpdf.name, prefix=localpdf.name)
        # os.system(poppler)
        os.unlink(local_pdf)
        logger.debug('Converted.')

        thumb = os.path.join(absolute_path_jpg, pdfobj.filename + 'thumb.jpg')
        reduce_image(infile=output, outfile=thumb, new_width=100)

        m = Maquette()
        m.customer = c
        m.remote_filename = pdfobj.filename
        m.last_change = last_write
        m.preview = os.path.join('warehouse', c.name, relative_path_jpg, pdfobj.filename + '.jpg')
        m.thumb = os.path.join('warehouse', c.name, relative_path_jpg, pdfobj.filename + 'thumb.jpg')
        m.width = width
        m.height = height
        m.save()

    conn.close()



    return HttpResponseRedirect('/customers_list/')


