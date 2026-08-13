from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from datetime import datetime
# from .forms import MultipleXMLUploadForm
from django.db.models import Q,F
from django.contrib.auth.decorators import login_required
# from .forms import BirthEntry
import io,os
from django.http import FileResponse
from django.conf import settings
from .models import Death,Form2a
from .forms import MultipleXMLUploadForm,DeathEntry
from .resource import Form2adata
from reportlab.pdfgen import canvas
from datetime import datetime

def clean_split(val):
    if not val:
        return ""
    return str(val).split('|')[0].strip()



def parse_date(date_str):
    """Helper to convert 'YYYY/MM/DD' or 'YYYY-MM-DD' into a date object."""
    if not date_str:
        return None
    # Normalize separators
    date_str = date_str.replace('/', '-')
    try:
        return datetime.strptime(date_str.split()[0], "%Y-%m-%d").date()
    except (ValueError, IndexError):
        return None


@login_required()
def upload_death_xml(request):
    if request.method == 'POST':
        form = MultipleXMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # request.FILES.getlist() retrieves all files uploaded under this key
            files = request.FILES.getlist('xml_files')
            success_count = 0
            for f in files:
                try:
                    # Parse XML directly from memory
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    # Extract fields safely using .findtext()
                    regno = root.findtext('RegistryNum', '')
                    regdate_str = root.findtext('DateRegistered', '')
                    
                    # Build full name: CFirstName + CMiddleName + CLastName
                    first = root.findtext('CFirstName', '')
                    middle = root.findtext('CMiddleName', '')
                    last = root.findtext('CLastName', '')
                    fullname = " ".join(filter(None, [first, middle, last]))
                    
                    # Extract raw string before pipe if applicable (e.g., "MALE|1")
                    
                    death_str = root.findtext('CBirthDate', '')
                    
                    # Create the model instance
                    death_record = Death(
                        regno=regno[:10],  # Protect against MaxLength restrictions
                        regdate=parse_date(regdate_str),
                        fullname=fullname[:200],
                        dateofdeath=parse_date(death_str),
                        # If you want to associate the source XML file:
                        xml=f 
                    )
                    death_record.save()
                    success_count += 1
                    
                except Exception as e:
                    if 'UNIQUE constraint'  in str(e):
                        messages.error(request, f"{regno} {regdate_str} {fullname} already exists! ")
                    else:
                        messages.error(request, f"Error processing file {f.name}: {str(e)}")
            
            if success_count > 0:
                messages.success(request, f"Successfully processed {success_count} XML files.")
            return redirect('uploaddeathxml')
    else:
        form = MultipleXMLUploadForm()
        
    return render(request, 'death/uploaddeathxml.html', {'form': form})


@login_required()
def deathlist(request):
    data=Death.objects.all().order_by('-regdate')[:50]
    if request.method=='POST':
        cri=request.POST['txtsearch']
        data=Death.objects.filter(Q(fullname__icontains=cri)|Q(regno__icontains=cri)).order_by('-regdate')[:50]
    return render(request,'death/deathlist.html',{'data':data})

@login_required()
def deathlogentry(request):
    if request.method=='POST':
        data=DeathEntry(request.POST,request.FILES)
        try:
            if data.is_valid():
                data.save()
                messages.success(request,'Data successfully added!')
        except Exception as e:
            messages.error(request,f'{str(e)}')
        return redirect('deathlist')
    form=DeathEntry()
    return  render(request,'death/deathlogentry.html',{'form':form})


@login_required()
def deathlogupdate(request,pk):
    data=Death.objects.get(id=pk)
    if request.method=='POST':
        form=DeathEntry(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,f'Data Successfully Updated!')
            return redirect('deathlist')
    form=DeathEntry(instance=data)
    return  render(request,'death/deathlogupdate.html',{'form':form})


@login_required()
def deathlogdelete(request,pk):
    data=get_object_or_404(Death,id=pk)
    data.delete()
    messages.error(request,f'{data} Successfully Removed!')
    return  redirect('deathlist')

@login_required()
def form2alist(request):
    data=Form2a.objects.select_related('death').values('death__regno',
                                                           'death__regdate',
                                                           'death__fullname','sex',
                                                           'death__dateofdeath','death__book','death__page','death__id','id'
                                                           )[:80]
    if request.method=='POST':
        cri=request.POST['txtsearch']
        data=Form2a.objects.select_related('death').values('death__regno',
                                                               'death__regdate',
                                                               'death__fullname','sex',
                                                               'death__dateofdeath','death__book','death__page','death__id','id'
                                                               ).filter(
                                                                   Q(death__regno__icontains=cri)|Q(death__fullname__icontains=cri)
                                                               )[:80]
        
    return render(request,'death/form2alist.html',{'data':data})

@login_required()
def form_2a(request,pk):
    context=Form2adata(pk).data1a()
    death=Death.objects.get(id=pk)
    if request.method=='POST':
        data=request.POST
        try:
            new=Form2a.objects.create(
                    death=death,
                    formdate=data['issuedate'],
                    sex=data['sex'],
                    age=data['age'],
                    civilstatus=data['civilstatus'],
                    citizenship=data['citizenship'],
                    dateofdeath=data['dateofdeath'],
                    placeofdeath=data['placeofdeath'],
                    issuedto=data['issuedto'],
                    amountpaid=data['amount'],
                    ornumber=data['or'],
                    datepaid=data['ordate'],
                    verifiedby=data['verifyby'],
                    verifiedbyposition=data['verified_position'],
                    remarks=data['remarks'],
            )
            new.save()
            messages.success(request,'Data successfully added!')
            return redirect('form2alist')
        except Exception as e:
            messages.error(request,f'{str(e)}')
    return render(request,'death/form2a.html',context)

@login_required()
def form_2a_report(request,pk):
    def centerstring(text,tv,p,alyn):
        tw=p.stringWidth(text)
        pw=p._pagesize[0]
        al=pw-(alyn)
        return p.drawString((al-tw)/2,tv,text)
    buffer=io.BytesIO()
    p=canvas.Canvas(buffer)
    data=Form2a.objects.select_related("death").filter(id=pk)
    for d in data:
        p.setTitle(f"Form 2A : " + str(d.death.fullname))
        p.setFontSize(12)
        bg=os.path.join(settings.STATICFILES_DIRS[0],'img/Form2a.jpg')
        p.drawImage(bg,0,0,p._pagesize[0],850)

        def strNone(s):
            if s:
                return s
            elif s==' ':
                    return '  '
            elif str(s)=='None':
                    return 'N/A'
            else:
                return '  '
        p.setFontSize(14)
        centerstring(d.formdate.strftime('%B %d,%Y'),687,p,-400)
        p.drawString(230,565,f'{str(strNone(d.death.page))}')
        p.drawString(350,565,f'{str(strNone(d.death.book))}')
        p.drawString(240,520,f'{str(strNone(d.death.regno))}')
        p.drawString(240,498,f'{str(strNone(d.death.regdate.strftime("%B %d, %Y")))}')
        p.drawString(240,474,f'{str(strNone(d.death.fullname))}')
        p.drawString(240,452,f'{str(strNone(d.sex))}')
        p.drawString(240,430,f'{str(strNone(d.age))} yrs old')
        p.drawString(240,408,f'{str(strNone(d.civilstatus))}')
        p.drawString(240,384,f'{str(strNone(d.citizenship))}')
        p.drawString(240,362,f'{str(strNone(d.dateofdeath.strftime("%B %d, %Y")))}')
        p.setFontSize(11)
        p.drawString(240,340,f'{str(strNone(d.placeofdeath))}')
        p.setFontSize(13)
        p.drawString(240,316,f'{str(strNone(d.issuedto))}')
        p.setFontSize(14)
        centerstring(d.verifiedby,199,p,197)
        centerstring(d.verifiedbyposition.title(),186,p,197)
        p.drawString(180,145,f'{str(strNone(float(d.amountpaid)))}')
        p.drawString(180,124,f'{str(strNone(d.ornumber))}')
        p.drawString(180,105,f'{str(strNone(d.datepaid.strftime("%B %d, %Y")))}')
        
     
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False,filename=f'Form2A {pk}.pdf')