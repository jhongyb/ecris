from django.test import TestCase
from django.shortcuts import render,get_object_or_404
from .models import Death, Form2a
import xml.etree.ElementTree as ET
from datetime import datetime

class Form2adata:
    def __init__(self,pk):
        self.pk=pk
    def data1a(self):
                data=get_object_or_404(Death,id=self.pk)
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
                dod=xml_data.get('CDeathDate')
                placeofdeath=f"{xml_data.get('CDeathAddress')}, {str(xml_data.get('CDeathMunicipality')).split('|')[0]}, {str(xml_data.get('CDeathMunicipality')).split('|')[1]}"
                citizenship=str(xml_data.get('CCitizenship')).split("|")[0]

                try:
                    dateofdeath=datetime.strptime(dod,'%Y/%m/%d')
                except(ValueError,TypeError):
                    dateofdeath=None
                context={'data':data,'xml':xml_data,'dateofdeath':dateofdeath,'placeofdeath':placeofdeath,
                         'citizenship':citizenship}
                return context