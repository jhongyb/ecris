from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget,DateWidget
from import_export.admin import ImportExportModelAdmin
from .models import Death


class DeathResource(resources.ModelResource):
    regdate = fields.Field(
        column_name='regdate',
        attribute='regdate',
        widget=DateWidget(format='%Y-%m-%d')
    )
    class Meta:
        model = Death
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('regno', 'regdate', 'fullname','dateofdeath')
        
    

@admin.register(Death)
class BirthAdmin(ImportExportModelAdmin):
    resource_class = DeathResource
    # 'get_emp_name' and 'bio_id_number' are the methods defined below
    list_display = ('regno', 'regdate', 'fullname', 'dateofdeath','book','page')
    list_editable=('regdate', 'fullname', 'dateofdeath','book','page')
    search_fields = ('regno', 'fullname')