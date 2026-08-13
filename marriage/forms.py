# forms.py
from django import forms
from .models import Marriage

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

# 1. We MUST create a custom field to handle the array processing
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

# 2. Use your custom MultipleFileField here instead of forms.FileField
class MultipleXMLUploadForm(forms.Form):
    xml_files = MultipleFileField(label="Select XML Files")



class MarriageEntry(forms.ModelForm):
    class Meta:
        model=Marriage
        fields='__all__'
        widgets={
            'dateofmarriage':forms.DateInput(attrs={'type':'date'}),
            'regdate':forms.DateInput(attrs={'type':'date'}),
            }
        labels={
            'regno':'Registry Number',
            'regdate':'Registered Date',
            'husband':'Husband',
            'wife':'Wife',
            'scandocx':'Scanned Docx'
        }
