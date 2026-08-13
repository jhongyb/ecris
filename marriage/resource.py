from django.test import TestCase
from django.shortcuts import render,get_object_or_404
from .models import Marriage,Form3a
import xml.etree.ElementTree as ET
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


class Form3adata:
    def __init__(self,pk):
        self.pk=pk
    def data1a(self):
                data=get_object_or_404(Marriage,id=self.pk)
                xml_data={}
                details={
                    'regno':data.regno,
                    'xml':{}
                }
                if data.xml:
                    try:
                        with data.xml.open('rb') as xml_file:
                            tree=ET.parse(xml_file)
                            root=tree.getroot()
                            for child in root:
                                xml_data[child.tag]=child.text
                            details['xml']=xml_data
                    except ET.ParseError:
                        print(f"Error: The XML file for record {data.regno} is corrupted or invalid.")
                    except Exception as e:
                        print(f"An unexpected error occurred while reading the file: {e}")
                else:
                    print(f"No XML file uploaded or found for record {data.regno}.")
                if xml_data.get('MarriageDate'):
                    dateofmarriage=datetime.strptime(xml_data.get('MarriageDate'),'%Y/%m/%d')
                else:
                     dateofmarriage=None
                if xml_data.get('DateRegistered'):
                     
                    dateofregistration=datetime.strptime(xml_data.get('DateRegistered'),'%Y/%m/%d')
                else:
                    dateofregistration=None
                place=f"{clean_split(xml_data.get('MarriagePlaceMunicipality'))}, {clean_split(xml_data.get('MarriagePlaceProvince'))}"
                hcitizen=clean_split(xml_data.get('HCitizenship'))
                wcitizen= clean_split(xml_data.get('WCitizenship'))
                context={'data':data,'xml':xml_data,'dom':dateofmarriage,'datereg':dateofregistration,'placeofmarriage':place,'hc':hcitizen,'wc':wcitizen}
                return context