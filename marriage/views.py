from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.db.models import Q,F
from django.contrib.auth.decorators import login_required
import io,os
from django.http import FileResponse
from django.conf import settings
from .models import Marriage,Form3a
from .forms import *
from reportlab.pdfgen import canvas
from datetime import datetime
from .resource import Form3adata


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
def marriagelist(request):
    data=Marriage.objects.all().order_by('-regdate')[:50]
    if request.method=='POST':
        cri=request.POST['txtsearch']
        data=Marriage.objects.filter(Q(husband__icontains=cri)|Q(wife__icontains=cri)|Q(regno__icontains=cri)).order_by('-regdate')[:50]
    return render(request,'marriage/marriagelist.html',{'data':data})

def upload_marriage_xml(request):
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
                    hfirst = root.findtext('HFirstName', '')
                    hmiddle = root.findtext('HMiddleName', '')
                    hlast = root.findtext('HLastName', '')
                    hfn = " ".join(filter(None, [hfirst, hmiddle, hlast]))

                    wfirst = root.findtext('WFirstName', '')
                    wmiddle = root.findtext('WMiddleName', '')
                    wlast = root.findtext('WLastName', '')
                    wfn = " ".join(filter(None, [wfirst, wmiddle, wlast]))
                    
                    # Extract raw string before pipe if applicable (e.g., "MALE|1")
                    
                    marriage_str = root.findtext('MarriageDate', '')
                    
                    # Create the model instance
                    marriage_record = Marriage(
                        regno=regno[:10],  # Protect against MaxLength restrictions
                        regdate=parse_date(regdate_str),
                        husband=hfn[:200],
                        wife=wfn[:200],
                        dateofmarriage=parse_date(marriage_str),
                        # If you want to associate the source XML file:
                        xml=f 
                    )
                    marriage_record.save()
                    success_count += 1
                    
                except Exception as e:
                    if 'UNIQUE constraint'  in str(e):
                        messages.error(request, f"{regno} {regdate_str} already exists! ")
                    else:
                        messages.error(request, f"Error processing file {f.name}: {str(e)}")
            
            if success_count > 0:
                messages.success(request, f"Successfully processed {success_count} XML files.")
            return redirect('uploadmarriagexml')
    else:
        form = MultipleXMLUploadForm()
        
    return render(request, 'marriage/uploadmarriagexml.html', {'form': form})

@login_required()
def marriagelogentry(request):
    if request.method=='POST':
            form=MarriageEntry(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,f'Data Successfully Save!')
                return redirect('marriagelist')
    form=MarriageEntry()
    return  render(request,'marriage/marriagelogentry.html',{'form':form})

@login_required()
def marriagelogupdate(request,pk):
    data=Marriage.objects.get(id=pk)
    if request.method=='POST':
            form=MarriageEntry(request.POST,request.FILES,instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,f'Data Successfully Updated!')
                return redirect('marriagelist')
    form=MarriageEntry(instance=data)
    return  render(request,'marriage/marriagelogentry.html',{'form':form})

@login_required()
def marriagelogdelete(request,pk):
    data=get_object_or_404(Marriage,id=pk)
    data.delete()
    messages.error(request,f'Data Successfully Removed!')
    return  redirect('marriagelist')


@login_required()
def form_3a(request,pk):
    context=Form3adata(pk).data1a()
    marriage=get_object_or_404(Marriage,id=pk)
    if request.method=="POST":
        data=request.POST
        new=Form3a.objects.create(
            marriage=marriage,
            dateissue=datetime.strptime(str(data['issuedate']),'%Y-%m-%d').strftime('%Y-%m-%d'),
            hname=data['husband'],
            wname=data['wife'],
            hage=data['hage'],
            wage=data['wage'],
            hsex=data['hsex'],
            wsex=data['wsex'],
            hcitizen=data['hcitizenship'],
            wcitizen=data['wcitizenship'],
            hstatus=data['hstatus'],
            wstatus=data['wstatus'],
            hfather=data['hfather'],
            wfather=data['wfather'],
            hmother=data['hmother'],
            wmother=data['wmother'],
            regno=data['regno'],
            regdate=data['regdate'],
            dateofmarriage=data['dateofmarriage'],
            placeofmarriage=data['placeofmarriage'],
            issuedto=data['issuedto'],
            amountpaid=data['amount'],
            ornumber=data['or'],
            ordate=datetime.strptime(str(data['ordate']),'%Y-%m-%d').strftime('%Y-%m-%d') if data['ordate'] else None,
            verifiedby=data['verifyby'],
            verifiedbyposition=data['verified_position'],
            remarks=data['remarks'],
            book=data['book'],
            page=data['page']
        )
        new.save()
        messages.success(request, 'Form 1A successfully save.')
        return redirect('form3alist')
    return render(request,'marriage/form3a.html',context)



@login_required()
def form_3a_report(request,pk):
        def centerstring(text,tv,p,alyn):
            tw=p.stringWidth(text)
            pw=p._pagesize[0]
            al=pw-(alyn)
            return p.drawString((al-tw)/2,tv,text)
        buffer=io.BytesIO()
        p=canvas.Canvas(buffer)
    
        data=get_object_or_404(Form3a,id=pk)
        data2=Marriage.objects.get(id=data.marriage_id)

        # p.setTitle(f"Form 3A : " + str(d.birth.fullname))
        p.setTitle(data.regno)
        p.setFontSize(13)
        bg=os.path.join(settings.STATICFILES_DIRS[0],'img/form3a.jpg')
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
        centerstring(f'{str(strNone(data.dateissue).strftime("%B %d, %Y"))}',685,p,-400)
        p.setFontSize(11)
        p.drawString(320,598,f'{str(strNone(data2.book))}')
        p.drawString(220,598,f'{str(strNone(data2.page))}')
        p.drawString(195,540,f'{str(strNone(data.hname))}')
        p.drawString(375,540,f'{str(strNone(data.wname))}')

        p.drawString(197,516,f'{str(strNone(data.hage))} yrs old')
        p.drawString(375,516,f'{str(strNone(data.wage))} yrs old')

        p.drawString(197,494,f'{str(strNone(data.hcitizen))}')
        p.drawString(375,494,f'{str(strNone(data.wcitizen))}')

        p.drawString(197,472,f'{str(strNone(data.hsex))}')
        p.drawString(375,472,f'{str(strNone(data.wsex))}')

        p.drawString(197,450,f'{str(strNone(data.hstatus))}')
        p.drawString(375,450,f'{str(strNone(data.wstatus))}')

        p.drawString(197,426,f'{str(strNone(data.hmother))}')
        p.drawString(375,426,f'{str(strNone(data.wmother))}')

        p.drawString(197,404,f'{str(strNone(data.hfather))}')
        p.drawString(375,404,f'{str(strNone(data.wfather))}')

        p.drawString(197,380,f'{str(strNone(data.regno))}')
        p.drawString(197,358,f'{str(strNone(data.regdate).strftime("%B %d, %Y"))}')
        p.drawString(197,337,f'{str(strNone(data.dateofmarriage).strftime("%B %d, %Y"))}')
        p.setFontSize(8)
        p.drawString(197,314,f'{str(strNone(data.placeofmarriage))}')
        p.setFontSize(11)
        p.drawString(197,289,f'{str(strNone(data.issuedto))}')
        p.setFontSize(13)
        centerstring(f'{str(data.verifiedby)}',192,p,300)
        centerstring(f'{str(data.verifiedbyposition)}',180,p,300)
        p.setFontSize(11)
        p.drawString(197,162,f'{str(strNone(data.amountpaid))}')
        p.drawString(197,140,f'{str(strNone(data.ornumber))}')
        p.drawString(197,120,f'{str(strNone(data.ordate).strftime("%B %d, %Y"))}')




        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer,as_attachment=False,filename=f'Form3A {pk}.pdf')


def form3alist(request):
    data=Form3a.objects.all()[:50]
    if request.method=="POST":
         cri=request.POST['txtsearch']
         data=Form3a.objects.all().filter(
              Q(hname__icontains=cri) | Q(wname__icontains=cri) |Q(regno__icontains=cri)
         )[:50]
    return render(request,'marriage/form3alist.html',{'data':data})


def form3adelete(request,pk):
    data=Form3a.objects.get(id=pk)
    if data:
         data.delete()
    else:
         pass
    return redirect('form3alist')


