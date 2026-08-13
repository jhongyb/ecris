from django.db import models

class Marriage(models.Model):
    regno=models.CharField(max_length=50,unique=True)
    regdate=models.DateField()
    husband=models.CharField(max_length=250)
    wife=models.CharField(max_length=250)
    dateofmarriage=models.DateField(null=True,blank=True)
    page=models.IntegerField(blank=True,null=True)
    book=models.IntegerField(blank=True,null=True)
    xml=models.FileField(upload_to='marriage/xml',null=True,blank=True)
    scandocx=models.FileField(upload_to='marriage/file',null=True,blank=True)
    class Meta:
            constraints=[
                models.UniqueConstraint(
                    fields=['regno','husband','wife'],name='uniquemarriage'
                )
            ]


class Form3a(models.Model):
      marriage=models.ForeignKey(Marriage,blank=True,null=True,on_delete=models.SET_NULL)
      dateissue=models.DateField(auto_now=True)
      hname=models.CharField(max_length=250)
      wname=models.CharField(max_length=250)
      hage=models.IntegerField()
      wage=models.IntegerField()
      hsex=models.CharField(max_length=15)
      wsex=models.CharField(max_length=15)
      hcitizen=models.CharField(max_length=15)
      wcitizen=models.CharField(max_length=15)
      hstatus=models.CharField(max_length=15)
      wstatus=models.CharField(max_length=15)
      hfather=models.CharField(max_length=200)
      wfather=models.CharField(max_length=200)
      hmother=models.CharField(max_length=200)
      wmother=models.CharField(max_length=200)
      regno=models.CharField(max_length=15)
      regdate=models.DateField()
      dateofmarriage=models.DateField()
      placeofmarriage=models.CharField(max_length=300,blank=True,null=True)
      issuedto=models.CharField(max_length=250,blank=True,null=True)
      verifiedby=models.CharField(max_length=250,blank=True,null=True)
      verifiedbyposition=models.CharField(max_length=250,blank=True,null=True)
      amountpaid=models.FloatField(default=0.00,null=True,blank=True)
      ornumber=models.CharField(max_length=50,null=True,blank=True)
      ordate=models.DateField(null=True,blank=True)
      remarks=models.TextField(null=True,blank=True)
      book=models.IntegerField(null=True,blank=True)
      page=models.IntegerField(null=True,blank=True)



      

