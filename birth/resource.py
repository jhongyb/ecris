from django.test import TestCase
from django.shortcuts import render,get_object_or_404
from .models import Birth,Form1a
import xml.etree.ElementTree as ET
from datetime import datetime

class Form1adata:
    def __init__(self,pk):
        self.pk=pk
        print(self.pk)
    def data1a(self):
                data=get_object_or_404(Birth,id=self.pk)
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
                bplace=f"{xml_data.get('CBirthAddress')}, {str(xml_data.get('CBirthMunicipality')).split('|')[0]}, {xml_data.get('CBirthProvince')}"
                mother=f"{xml_data.get('MFirstName')}  {str(xml_data.get('MMiddleName'))} {xml_data.get('MLastName')}"
                nmother=f"{str(xml_data.get('MCitizenship')).split('|')[0]}"
                father=f"{xml_data.get('FFirstName')}  {str(xml_data.get('FMiddleName'))} {xml_data.get('FLastName')}"
                nfather=f"{str(xml_data.get('FCitizenship')).split('|')[0]}"
                dom=xml_data.get('MarriageDate')
                try:
                    dateofmarriage=datetime.strptime(dom,'%Y/%m/%d')
                except(ValueError,TypeError):
                    dateofmarriage=None
                     
                placeofmarriage=f"{str(xml_data.get('MarriageMunicipality')).split('|')[0]}, {xml_data.get('MarriageProvince')}"
                context={'data':data,'xml':xml_data,'bplace':bplace,'mother':mother,'father':father,
                         'nm':nmother,'nf':nfather,'dom':dateofmarriage,'pom':placeofmarriage}
                return context