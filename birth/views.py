from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from datetime import datetime
from .forms import MultipleXMLUploadForm
from .models import Birth,Form1a
from django.db.models import Q,F
from django.contrib.auth.decorators import login_required
from .forms import BirthEntry
import io,os
from django.http import FileResponse
from .resource import Form1adata
from django.conf import settings


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
def upload_birth_xml(request):
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
                    sex_raw = root.findtext('CSex', '')
                    sex = sex_raw.split('|')[0] if sex_raw else ''
                    
                    birthday_str = root.findtext('CBirthDate', '')
                    
                    # Create the model instance
                    birth_record = Birth(
                        regno=regno[:10],  # Protect against MaxLength restrictions
                        regdate=parse_date(regdate_str),
                        fullname=fullname[:200],
                        sex=sex[:10],
                        birthday=parse_date(birthday_str),
                        # If you want to associate the source XML file:
                        xml=f 
                    )
                    birth_record.save()
                    success_count += 1
                    
                except Exception as e:
                    if 'UNIQUE constraint'  in str(e):
                        messages.error(request, f"{regno} {regdate_str} {fullname} already exists! ")
                    else:
                        messages.error(request, f"Error processing file {f.name}: {str(e)}")
            
            if success_count > 0:
                messages.success(request, f"Successfully processed {success_count} XML files.")
            return redirect('uploadbirthxml')
    else:
        form = MultipleXMLUploadForm()
        
    return render(request, 'birth/uploadbirthxml.html', {'form': form})

@login_required()
def birthlist(request):
    data=Birth.objects.all().order_by('-regdate')[:50]
    if request.method=='POST':
        cri=request.POST['txtsearch']
        data=Birth.objects.filter(Q(fullname__icontains=cri)|Q(regno__icontains=cri)).order_by('-regdate')[:50]
    return render(request,'birth/birthlist.html',{'data':data})

@login_required()
def birthlogentry(request):
    form=BirthEntry()
    return  render(request,'birth/birthlogentry.html',{'form':form})

@login_required()
def birthlogupdate(request,pk):
    data=Birth.objects.get(id=pk)
    if request.method=='POST':
        form=BirthEntry(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,f'Data Successfully Updated!')
            return redirect('birthlist')
    form=BirthEntry(instance=data)
    return  render(request,'birth/birthlogupdate.html',{'form':form})

@login_required()
def birthlogdelete(request,pk):
    data=get_object_or_404(Birth,id=pk)
    data.delete()
    messages.error(request,f'{data} Successfully Removed!')
    return  redirect('birthlist')


@login_required()
def form_1a(request,pk):
    context=Form1adata(pk).data1a()
    birth=get_object_or_404(Birth,id=pk)
    if request.method=="POST":
        data=request.POST
        new=Form1a.objects.create(
            birth=birth,
            formdate=datetime.strptime(str(data['issuedate']),'%Y-%m-%d').strftime('%Y-%m-%d'),
            placeofbirth=data['bplace'],
            mother=data['mother'],
            Nmother=data['mother_nationality'],
            father=data['father'],
            Nfather=data['father_nationality'],
            issuedto=data['issuedto'],
            dateofmarriage=datetime.strptime(str(data['dateofmarriage']),'%Y-%m-%d') if data['dateofmarriage'] else None,
            amountpaid=data['amount'],
            ornumber=data['or'],
            datepaid=datetime.strptime(str(data['ordate']),'%Y-%m-%d').strftime('%Y-%m-%d') if data['ordate'] else None,
            verifiedby=data['verifyby'],
            verifiedbyposition=data['verified_position'],
            remarks=data['remarks']
        )
        new.save()
        messages.success(request, 'Form 1A successfully save.')
        return redirect('form1alist')
    return render(request,'birth/form1a.html',context)


@login_required()
def form1alist(request):
    data=Form1a.objects.select_related('birth').values('birth__regno',
                                                       'birth__regdate',
                                                       'birth__fullname','birth__sex',
                                                       'birth__birthday','birth__book','birth__page','birth__id','id'
                                                       )[:80]
    if request.method=="POST":
        cri=request.POST['txtsearch']
        data=Form1a.objects.select_related('birth').values('birth__regno',
                                                               'birth__regdate',
                                                               'birth__fullname','birth__sex',
                                                               'birth__birthday','birth__book','birth__page','birth__id','id'
                                                               ).filter(
                                                                   Q(birth__regno__icontains=cri) | Q(birth__fullname__icontains=cri)
                                                               )[:80]
    return render(request,'birth/form1alist.html',{'data':data})



@login_required()
def form1adelete(request,pk):
    data=Form1a.objects.get(id=pk)
    data.delete()
    messages.error(request,f'{data.birth} - Form 1a Successfully Removed!')
    return  redirect('form1alist')

@login_required()
def form_1a_report(request,pk):
    def centerstring(text,tv,p,alyn):
        tw=p.stringWidth(text)
        pw=p._pagesize[0]
        al=pw-(alyn)
        return p.drawString((al-tw)/2,tv,text)
    buffer=io.BytesIO()
    p=canvas.Canvas(buffer)
  
    data=Form1a.objects.select_related("birth").filter(id=pk)
    for d in data:
        p.setTitle(f"Form 1A : " + str(d.birth.fullname))
        p.setFontSize(12)
        bg=os.path.join(settings.STATICFILES_DIRS[0],'img/form1a.jpg')
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
        # p.drawString(185,600,f'{str(strNone(data.date))}')
        p.drawString(185,600,f'{str(strNone(d.birth.page))}')
        p.drawString(290,600,f'{str(strNone(d.birth.book))}')
        #Data
        p.drawString(260,573,str(d.birth.regno))
        p.drawString(260,550,str(datetime.strptime(str(d.birth.regdate),'%Y-%m-%d').strftime('%B %d, %Y')))
        p.drawString(260,528,str(d.birth.fullname))
        p.drawString(260,504,str(d.birth.sex))
        p.drawString(260,482,str(datetime.strptime(str(d.birth.birthday),'%Y-%m-%d').strftime('%B %d, %Y')))
        p.setFontSize(11)
        p.drawString(260,457,str(d.placeofbirth))
        p.setFontSize(12)
        p.drawString(260,436,str(d.mother))
        p.drawString(260,412,str(d.Nmother))
        p.drawString(260,388,str(d.father))
        p.drawString(260,363,str(d.Nfather))
        if d.dateofmarriage:
            p.drawString(260,343,str(datetime.strptime(str(d.dateofmarriage),'%Y-%m-%d').strftime('%B %d, %Y')))
        else:
            p.drawString(260,343,'N/A')
        p.drawString(260,319,strNone(str(d.placeofmarriage)))
        p.drawString(260,297,str(d.issuedto))
        centerstring(str(d.verifiedby),178,p,200)
        centerstring(str(d.verifiedbyposition),163,p,200)
        p.drawString(150,138,str(d.amountpaid))
        p.drawString(150,117,str(d.ornumber))
        if d.datepaid:
            p.drawString(150,97,str(datetime.strptime(str(d.datepaid),'%Y-%m-%d').strftime('%m/%d/%Y')))
        else:
             p.drawString(150,97,'N/A')
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False,filename=f'Form1A {pk}.pdf')
