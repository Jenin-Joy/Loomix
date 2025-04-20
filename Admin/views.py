from django.shortcuts import render,redirect
from Admin.models import *
from User.models import *
from django.db.models import Sum


# Create your views here.
def add(request):
    return render(request,'Admin/add.html')

def Largest(request):
    return render(request,'Admin/Largest.html')
 
def add(request):
    if request.method=="POST":
        a=int(request.POST.get("Number 1"))
        b=int(request.POST.get("Number 2"))
        c=a+b
        return render(request,"Admin/Add.html",{'result':c})
    else:
        return render(request,"admin/Add.html")

def Largest(request):
    if request.method=="POST":
        a=int(request.POST.get("Number 1"))
        b=int(request.POST.get("Number 2"))
        if a>b:
            return render(request,"Admin/Largest.html",{'result':a})
        else:
            return render(request,"Admin/Largest.html",{'result':b})
    else:
        return render(request,"Admin/Largest.html")

def Calculator(request):
    if request.method=="POST":
        a=int(request.POST.get("Number 1"))
        b=int(request.POST.get("Number 2"))
        btn=request.POST.get("cal")
        # if btn==
        return render(request,"Admin/Calculator.html",{'result':a})
        # else:
        #     return render(request,"Admin/Calculator.html",{'result':b})
    else:
        return render(request,"Admin/Calculator.html")

def District(request):
    dis=tbl_district.objects.all()
    if request.method=="POST":
        district=(request.POST.get("district"))
        tbl_district.objects.create(district_name=district)
        return render(request,"Admin/district.html",{'result':dis})
    else:
        return render(request,"admin/district.html",{'result':dis})

def Category(request):
    Category=tbl_category.objects.all()
    if request.method=="POST":
        Categorydata=(request.POST.get("Category"))
        tbl_category.objects.create(category_name=Categorydata)
        return render(request,"Admin/Category.html",{'result':Category})
    else:
        return render(request,"admin/Category.html",{'result':Category})

def adminreg(request):
    adminreg=tbl_adminreg.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        tbl_adminreg.objects.create(admin_name=name,admin_email=email,admin_password=password)
        
        return redirect("Admin:adminreg")
    else:
        return render(request,"admin/AdminReg.html",{'result':adminreg})

def deladmin(request,id):
    tbl_adminreg.objects.get(id=id).delete()
    return redirect("Admin:adminreg")

def deldis(request,id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Admin:district")


def brand(request):
    br=tbl_brand.objects.all()
    if request.method=="POST":
        brand=request.POST.get('br')
        tbl_brand.objects.create(brand_name=brand)
        return render(request,'Admin/brand.html',{'brand':br})
    else:
        return render(request,'Admin/brand.html',{'brand':br})  
    
def bdelete(request,id):
    tbl_brand.objects.get(id=id).delete()
    return redirect("Admin:brand")
def place(request):
    dis=tbl_district.objects.all()
    pl=tbl_place.objects.all()
    if request.method=="POST":
         dist=tbl_district.objects.get(id=request.POST.get("sel_district"))
         tbl_place.objects.create(place_name=request.POST.get("txt_place"),district=dist)
         return redirect("Admin:place")
    else:
         return render(request,'Admin/place.html',{'result':dis,'r':pl})
def delplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Admin:place")
def editplace(request,id):
    p=tbl_place.objects.get(id=id)
    p1=tbl_place.objects.all()   
    if request.method=="POST":
        p.place_name=request.POST.get("place_name")
        p.save()
        return redirect("Admin:place")
    else:
        return render(request,'Admin/place.html',{'rr':p,'r':p1})
def bedit(request,id):
    brand=tbl_brand.objects.get(id=id)
    if request.method=="POST":
        brand.brand_name=request.POST.get("br")
        brand.save()
        return redirect('Admin:brand')
    else:
        return render(request,'Admin/brand.html',{'bran':brand})
    
def subcategory(request):
    cat=tbl_category.objects.all()#select
    subcategory=tbl_subcategory.objects.all()
    if request.method=="POST":
        cat=tbl_category.objects.get(id=request.POST.get("seld"))
        tbl_subcategory.objects.create(subcategory_name=request.POST.get("subcategory"),category=cat)
        return redirect("Admin:subcategory")
    else:
        return render(request,'Admin/Subcategory.html',{'category':cat,'sub':subcategory})
    
def cdelete(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Admin:subcategory") 
 
def cedit(request,id):
    category=tbl_category.objects.all()
    sanam=tbl_subcategory.objects.get(id=id)
    if request.method=="POST":
        sanam.subcategory_name=request.POST.get("subcategory")
        sanam.save()
        return redirect('Admin:subcategory')
    else:
        return render(request,'Admin/subcategory.html',{'su':sanam,'category':category})

def product(request):
    category=tbl_category.objects.all()
    pro=tbl_product.objects.all()
    for i in pro:
        total_stock = tbl_stock.objects.filter(product=i.id).aggregate(total=Sum('stock_quantity'))['total']
        total_cart = tbl_cart.objects.filter(product=i.id, cart_status=0).aggregate(total=Sum('cart_quantity'))['total']
        # print(total_stock)
        # print(total_cart)
        if total_stock is None:
            total_stock = 0
        if total_cart is None:
            total_cart = 0
        total =  total_stock - total_cart
        i.total_stock = total
    if request.method=="POST":
        tbl_product.objects.create(
            product_name=request.POST.get("txt_name"),
            product_price=request.POST.get("txt_price"),
            product_photo=request.FILES.get("file_photo"),
            product_total_price=request.POST.get("txt_total_price"),
            product_description=request.POST.get("txt_description"),
            category=tbl_category.objects.get(id=request.POST.get("sel_category")),
        )
        return redirect("Admin:product")
    else:
        return render(request,"Admin/Product.html",{'category':category,'product':pro})

def size(request):
    size=tbl_size.objects.all()
    if request.method=="POST":
        tbl_size.objects.create(size_name=request.POST.get("txt_size"))
        return redirect("Admin:size")
    else:
        return render(request,"Admin/Size.html",{'size':size})

def deletesize(request,id):
    tbl_size.objects.get(id=id).delete()
    return redirect("Admin:size")

def addsize(request,id):
    size=tbl_size.objects.all()
    productsize=tbl_productsize.objects.filter(product=id)
    if request.method=="POST":
        tbl_productsize.objects.create(product=tbl_product.objects.get(id=id),size=tbl_size.objects.get(id=request.POST.get("sel_size")))
        return redirect("Admin:addsize",id)
    else:
        return render(request,"Admin/Addsize.html",{'size':size,'productsize':productsize,"id":id})

def deleteaddsize(request,id,sizeid):
    tbl_productsize.objects.get(id=id).delete()
    return redirect("Admin:addsize",sizeid)

def Stock(request,id):
    data=tbl_stock.objects.filter(product=id)
    if request.method=="POST":
        name=request.POST.get("txt_stock")
        tbl_stock.objects.create(stock_quantity=name,product=tbl_product.objects.get(id=id))
        return redirect("Admin:Stock",id)
    else:
        return render(request,"Admin/stock.html",{'data':data})
        
    
def delstock(request,did):
    tbl_stock.objects.get(id=did).delete()
    return redirect('Admin:Product')

def homepage(request):
    return render(request, 'Admin/AdminHomepage.html')

def logout(request):
    del request.session["aid"]
    return redirect("Guest:index")

def viewbooking(request):
    rel=tbl_booking.objects.filter(booking_status__gt=0)
    return render(request,"Admin/viewbooking.html",{'rel':rel})