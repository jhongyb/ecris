from django.shortcuts import render
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from birth.models import Birth
from death.models import Death
from marriage.models import Marriage
from django.db.models import Count
from django.db.models.functions import ExtractYear



@login_required
def Home(request):
    birth_figure=Birth.objects.all()
    marriage_figure=Marriage.objects.all()
    death_figure=Death.objects.all()
    count_birth=birth_figure.values('sex').annotate(total=Count('id')).order_by('-sex')
    count_birth_year=birth_figure.annotate(year=ExtractYear('regdate')).values('year').annotate(total=Count('id')).order_by('-year')
    count_marriage_year=marriage_figure.annotate(year=ExtractYear('regdate')).values('year').annotate(total=Count('id')).order_by('-year')
    count_death_year=death_figure.annotate(year=ExtractYear('regdate')).values('year').annotate(total=Count('id')).order_by('-year')
    context={
        'birth_figure':len(birth_figure),
        'marriage_figure':len(marriage_figure),
        'death_figure':len(death_figure),
        'birth_count':count_birth,
        'birth_count_year':count_birth_year,
        'marriage_count_year':count_marriage_year,
        'death_count_year':count_death_year,
    }
    return render(request,'base.html',context)

@login_required
def Restricted(request):
    return render(request,'restricted.html')