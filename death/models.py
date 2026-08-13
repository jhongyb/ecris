from django.db import models

class Death(models.Model):
    regno=models.CharField(max_length=10)
    regdate=models.DateField()
    fullname=models.CharField(max_length=200)
    dateofdeath=models.DateField(null=True,blank=True)
    book=models.IntegerField(blank=True,null=True)
    page=models.IntegerField(blank=True,null=True)
    xml=models.FileField(upload_to='death/xml/',null=True,blank=True)
    scandocs=models.FileField(upload_to='death/file/',null=True,blank=True)
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['regno','regdate','fullname'],name='uniquedeath'
            )
        ]
    def __str__(self):
        return self.fullname


class Form2a(models.Model):
    death=models.ForeignKey(Death,on_delete=models.CASCADE,related_name='death')
    formdate=models.DateField()
    sex=models.CharField(max_length=10,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    civilstatus=models.CharField(max_length=250,null=True,blank=True)
    citizenship=models.CharField(max_length=250,null=True,blank=True)
    dateofdeath=models.DateField(null=True,blank=True)
    placeofdeath=models.CharField(max_length=250,null=True,blank=True)
    issuedto=models.CharField(max_length=250,null=True,blank=True)
    amountpaid=models.FloatField()
    ornumber=models.CharField(max_length=10,null=True,blank=True)
    datepaid=models.DateField(null=True,blank=True)
    verifiedby=models.CharField(max_length=250,null=True,blank=True)
    verifiedbyposition=models.CharField(max_length=250,null=True,blank=True)
    remarks=models.CharField(max_length=250,null=True,blank=True)