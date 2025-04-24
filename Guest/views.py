from django.shortcuts import render,redirect

from Guest.models import *
from Admin.models import *

def index(request):
    return render(request,'Guest/index.html')

def Registration(request):
    dis=tbl_district.objects.all()
    if request.method=="POST":
        pl=tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_user.objects.create(reg_name=request.POST.get("reg_name"),reg_email=request.POST.get("reg_email"),reg_contact=request.POST.get("reg_contact"),reg_password=request.POST.get("reg_password"),reg_address=request.POST.get("reg_address"),user_photo=request.FILES.get("file_photo"),place=pl)
        return redirect('Guest:login')
    else:
        return render(request,'Guest/Registration.html',{'dis':dis})
       
def Ajaxplace(request):
    place=tbl_place.objects.filter(district=request.GET.get("did"))
    return render(request,'Guest/Ajaxplace.html',{'place':place})

def login(request):
    if request.method=="POST":
        email=request.POST.get("reg_email")
        password=request.POST.get("reg_password")
        usercount=tbl_user.objects.filter(reg_email=email,reg_password=password).count()
        admincount=tbl_adminreg.objects.filter(admin_email=email,admin_password=password).count()
        if usercount > 0:
            user=tbl_user.objects.get(reg_email=email,reg_password=password)
            request.session["uid"]=user.id
            return redirect("User:Homepage")
        elif admincount > 0:
            admin=tbl_adminreg.objects.get(admin_email=email,admin_password=password)
            request.session["aid"]=admin.id
            return redirect("Admin:homepage")
        else:
            return render(request,'Guest/Login.html')
    else:
        return render(request,'Guest/Login.html')