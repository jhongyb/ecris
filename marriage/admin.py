from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget,DateWidget
from import_export.admin import ImportExportModelAdmin
from .models import Marriage

class MarriageResource(resources.ModelResource):
    regdate = fields.Field(
        column_name='regdate',
        attribute='regdate',
        widget=DateWidget(format='%Y-%m-%d')
    )
    class Meta:
        model = Marriage
        exclude = ('id',)
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('regno', 'regdate', 'husband','wife','dateofmarriage')
        
@admin.register(Marriage)
class BirthAdmin(ImportExportModelAdmin):
    resource_class = MarriageResource
    # 'get_emp_name' and 'bio_id_number' are the methods defined below
    list_display = ('regno', 'regdate', 'husband', 'wife', 'dateofmarriage','book','page')
    list_editable=('regdate', 'husband', 'wife', 'dateofmarriage','book','page')
    search_fields = ('regno', 'husband','wife')