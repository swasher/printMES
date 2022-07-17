from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from core.models import Employee
from core.models import Customer
from core.models import Contractor
from core.models import PrintingPress
from core.models import Paper
from core.models import PaperSize
from core.models import TechnologicalOperation

admin.site.site_header = 'Print MES (Manufacturing Execution System)'


class EmployeeInline(admin.TabularInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Доп. инфо'


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ('get_username', 'user', 'phone')

    def get_username(self, obj):
        return ' '.join([obj.user.first_name, obj.user.last_name])
    get_username.short_description = 'ФИО'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'fio', 'phone', 'remarks', 'user',)
    fields = ('name', 'address', 'fio', 'phone', 'remarks', 'user',)


class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'remarks']


class TechnologicalOperationAdmin(admin.ModelAdmin):
    list_display = ['name']


class PrintingPressAdmin(admin.ModelAdmin):
    list_display = ('name', 'plate_w', 'plate_h', 'klapan', 'cost')


class PaperSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'comment', 'is_printing')


class PaperAdmin(admin.ModelAdmin):
    list_display = ('name', 'grammage', 'type', 'paper_warehouse_unit', 'paper_warehouse_format')


admin.site.register(Contractor, ContractorAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(PrintingPress, PrintingPressAdmin)
admin.site.register(TechnologicalOperation, TechnologicalOperationAdmin)
admin.site.register(PaperSize, PaperSizeAdmin)
admin.site.register(Paper, PaperAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)

