from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget,DateWidget
from import_export.admin import ImportExportModelAdmin
from .models import Birth

class BirthResource(resources.ModelResource):
    regdate = fields.Field(
        column_name='regdate',
        attribute='regdate',
        widget=DateWidget(format='%Y-%m-%d')
    )
    class Meta:
        model = Birth
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('regno', 'regdate', 'fullname','sex','birthday')
        
    

@admin.register(Birth)
class BirthAdmin(ImportExportModelAdmin):
    resource_class = BirthResource
    # 'get_emp_name' and 'bio_id_number' are the methods defined below
    list_display = ('regno', 'regdate', 'fullname', 'sex', 'birthday','book','page')
    list_editable=('regdate', 'fullname', 'sex', 'birthday','book','page')
    search_fields = ('regno', 'fullname')
    # list_filter=(('bio_date',DateRangeFilter),('bio_id'))

    # Helper method to show Employee Name in the list
    # def get_emp_name(self, obj):
    #     emp = Employee.objects.filter(Birth_number=obj.bio_id).first()
    #     return f"{emp.lastname}, {emp.firstname} {emp.middlename}" if emp else "Unknown"
    # get_emp_name.short_description = 'Employee Name'

    # Helper method to show the Birth Number in the list
    # def bio_id_number(self, obj):
    #     return obj.bio_id
    # bio_id_number.short_description = 'Bio ID'

# admin.site.register(Birth)
admin.site.site_header="Local Civil Registry - Admin Page"