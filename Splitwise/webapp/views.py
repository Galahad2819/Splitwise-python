from django.shortcuts import render
from webapp.forms import UserForm
from webapp.forms import HistForm
from webapp.forms import TransactionForm
from webapp.models import Transaction_Pairs
from webapp.models import Transaction_history
#from webapp.forms import UserProfileInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

#import all the views eg-from django.view.generic import(TemplateView,ListView)


@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered=False

    if request.method == "POST":
        user_form=UserForm(data=request.POST)
        #profile_form=UserProfileInfoForm(data=reuest.Post)
        if user_form.is_valid():
            #and profile_frm.is_valid()
            user =user_form.save()
            user.set_password(user.password)
            user.save()
            #profile=profile_form.save(commit=False)
            #profile.user=user
            #if 'profile_pic' in request.files:
                #profile.profile_pic=request.FILES['profile_pic']
            #profile.save
            registered=True

            #print(profile_forms.errors)
    else:
        user_form=UserForm()
        #profile_form=UserProfileInfoFrom()
    return render(request,'webapp/registeration.html',{'user_form':user_form,'registered':registered})
    #add key value pair 'profile_form':profile_form,

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, 'webapp/login.html', {})


def transaction(request):
    numpeople=0
    amt=0
    progress=False
    if request.method == "POST":
        transact_form=TransactionForm(data=request.POST)
        #history_form=HistForm(data=request.POST)
        #and history_form.is_valid()
        if transact_form.is_valid():
            progress=True
            person1_=request.user.get_username()
            amt=request.POST["amount"]
            #reason=request.POST["reason"]
            #date=request.POST["date"]
            amt1=float(amt)
            people=request.POST["people"]
            user_list=[]
            a=0
            for x in range(0,len(people)):
                if people[x]==',':
                    temp=people[a:x]
                    a=x + 1
                    user_list.append(temp)
                    temp=""
            user_list.append(people[a:])
            numpeople_=len(user_list)+1
            for i in range(1,numpeople_):
                person2_=user_list[i-1]
                contrib=(amt1)/float(numpeople_)
                t_pair_count = Transaction_Pairs.objects.filter(person1=person1_,person2=person2_).count()
                if t_pair_count==1:
                    obj=Transaction_Pairs.objects.get(person1=person1_,person2=person2_)
                    amt_=float(obj.amount)
                    amt_+=contrib
                    obj.amount=amt_
                    obj.save()
                    t_pair_count=0
                elif t_pair_count==0:
                    transact=Transaction_Pairs(person1=person1_,person2=person2_,amount=contrib)
                    transact.save()
                    t_pair_count=0
                else:
                    break
                #history=Transaction_history(date=date,reason=reason,amount=contrib)
                #history.save()



    else:
        transact_form=TransactionForm()
        #history_form=HistForm()
        return render(request,'webapp/transaction.html',{'transact_form':transact_form,'progress':progress,})
    data= Transaction_Pairs.objects.filter(person1=request.user.get_username())
    return render(request,'webapp/index.html',{'transact_form':transact_form,'progress':progress,"messages":data})
#'history_form':history_form,
def index(request):
    data= Transaction_Pairs.objects.filter(person1=request.user.get_username())
    return render(request,'webapp/index.html',{"messages":data})


# Create your views here.
#For every page we need to Create
#class Name(TemplateView)
#template_name='name.html'
#etc etc
