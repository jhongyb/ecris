from django.db import models

class Birth(models.Model):
    regno=models.CharField(max_length=10)
    regdate=models.DateField()
    fullname=models.CharField(max_length=200)
    sex=models.CharField(max_length=10)
    birthday=models.DateField()
    book=models.IntegerField(blank=True,null=True)
    page=models.IntegerField(blank=True,null=True)
    xml=models.FileField(upload_to='birth/xml/',null=True,blank=True)
    scandocs=models.FileField(upload_to='birth/file/',null=True,blank=True)
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['regno','regdate','fullname'],name='uniquebirth'
            )
        ]
    def __str__(self):
        return self.fullname


class Form1a(models.Model):
    birth=models.ForeignKey(Birth,on_delete=models.CASCADE,related_name='birth')
    formdate=models.DateField()
    placeofbirth=models.CharField(max_length=250,null=True,blank=True)
    mother=models.CharField(max_length=250,null=True,blank=True)
    Nmother=models.CharField(max_length=250,null=True,blank=True)
    father=models.CharField(max_length=250,null=True,blank=True)
    Nfather=models.CharField(max_length=250,null=True,blank=True)
    dateofmarriage=models.DateField(null=True,blank=True)
    placeofmarriage=models.CharField(max_length=250,null=True,blank=True)
    issuedto=models.CharField(max_length=250,null=True,blank=True)
    amountpaid=models.FloatField()
    ornumber=models.CharField(max_length=10,null=True,blank=True)
    datepaid=models.DateField(null=True,blank=True)
    verifiedby=models.CharField(max_length=250,null=True,blank=True)
    verifiedbyposition=models.CharField(max_length=250,null=True,blank=True)
    remarks=models.CharField(max_length=250,null=True,blank=True)