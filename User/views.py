from django.shortcuts import render,redirect
from User.models import *
from Admin.models import *
from Guest.models import *
from django.db.models import Sum
from django.http import JsonResponse
def home(request):
 return render(request,'User/Homepage.html',{'home':home})

def profile(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    return render(request,'User/Myprofile.html',{'user':user})

def editprofile(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    if request.method == "POST":
        user.reg_name = request.POST.get("name")
        user.reg_email = request.POST.get("email")
        user.reg_contact = request.POST.get("contact")
        user.reg_address = request.POST.get("address")
        user.save()
        return redirect("User:profile")
    else:
        return render(request,'User/Editprofile.html',{'user':user})

def changepassword(request):
    user=tbl_user.objects.get(id=request.session["uid"])
    if request.method == "POST":
        if user.reg_password == request.POST.get("txt_oldpassword"):
            if request.POST.get("txt_newpassword") == request.POST.get("txt_retypepassword"):
                user.reg_password = request.POST.get("txt_newpassword")
                user.save()
                return render(request,'User/Myprofile.html',{"msg":"Password Updated"})
            else:
                return render(request,'User/Changepassword.html',{"msg":"Error in Confirm Password"})
        else:
            return render(request,'User/Changepassword.html',{"msg":"Error in Current Password"})
    else:
        return render(request,'User/Changepassword.html')



def viewproduct(request):
    ar=[1,2,3,4,5]
    parry=[]
    avg=0
    product=tbl_product.objects.all()
    categorys=tbl_category.objects.all()
    for i in product:
        wishlistcount = tbl_wishlist.objects.filter(user=request.session["uid"],product=i.id).count()
        if wishlistcount > 0:
            i.wishlist = True
        else:
            i.wishlist = False
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

        tot=0
        ratecount=tbl_rating.objects.filter(product=i.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(product=i.id)
            for j in ratedata:
                tot=tot+j.rating_data
                avg=tot//ratecount
                #print(avg)
            parry.append(avg)
        else:
            parry.append(0)
        # print(parry)
    datas=zip(product,parry)
    return render(request, 'User/ViewProduct.html',{'product':datas,'ar':ar,'categorys':categorys})



def addcart(request,pid):
    productdata=tbl_product.objects.get(id=pid)
    userdata=tbl_user.objects.get(id=request.session["uid"])
    bookingcount=tbl_booking.objects.filter(user=userdata,booking_status=0).count()
    if bookingcount>0:
        bookingdata=tbl_booking.objects.get(user=userdata,booking_status=0)
        cartcount=tbl_cart.objects.filter(booking=bookingdata,product=productdata).count()
        if cartcount>0:
            msg="Already added"
            return render(request,"User/ViewProduct.html",{'msg':msg})
        else:
            tbl_cart.objects.create(booking=bookingdata,product=productdata)
            msg="Added To cart"
            return render(request,"User/ViewProduct.html",{'msg':msg})
    else:
        bookingdata = tbl_booking.objects.create(user=userdata)
        tbl_cart.objects.create(booking=tbl_booking.objects.get(id=bookingdata.id),product=productdata)
        msg="Added To cart"
        return render(request,"User/ViewProduct.html",{'msg':msg})


def Mycart(request):
    
    if request.method=="POST":
        bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
        cart = tbl_cart.objects.filter(booking=bookingdata)
        flage = 0
        for i in cart:
            sizecount = tbl_productsize.objects.filter(product=i.product.id).count()
            if sizecount > 0:
                if i.size is None:
                    flage += 1
        if flage > 0:
            return render(request,"User/MyCart.html",{'msg':'Please Select Size'})
        else:
            for i in cart:
                i.cart_status = 1
                i.save()
            bookingdata.booking_amount=request.POST.get("carttotalamt")
            bookingdata.booking_status=1
            bookingdata.save()
            return redirect("User:payment",request.session["bookingid"])
    else:
        bookcount = tbl_booking.objects.filter(user=request.session["uid"],booking_status=0).count()
        if bookcount > 0:
            book = tbl_booking.objects.get(user=request.session["uid"],booking_status=0)
            request.session["bookingid"] = book.id
            cart = tbl_cart.objects.filter(booking=book)
            for i in cart:
                total_stock = tbl_stock.objects.filter(product=i.product.id).aggregate(total=Sum('stock_quantity'))['total']
                total_cart = tbl_cart.objects.filter(product=i.product.id, cart_status=0).aggregate(total=Sum('cart_quantity'))['total']
                # print(total_stock)
                # print(total_cart)
                if total_stock is None:
                    total_stock = 0
                if total_cart is None:
                    total_cart = 0
                total =  total_stock - total_cart
                i.total_stock = total
            return render(request,"User/MyCart.html",{'cartdata':cart})
        else:
            return render(request,"User/MyCart.html")
    
        

def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("User:Mycart")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_quantity=qty
   cartdata.save()
   return redirect("User:Mycart")  

def sizeupdate(request):
    size=request.GET.get('size')
    cartid=request.GET.get('cartid')
    cartdata=tbl_cart.objects.get(id=cartid)
    cartdata.size=tbl_size.objects.get(id=size)
    cartdata.save()
    return redirect("User:Mycart")


def payment(request,bid):
    bookingdata=tbl_booking.objects.get(id=bid)
    amt=bookingdata.booking_amount
    if request.method=="POST":
        bookingdata.booking_status=2
        bookingdata.save()
        return redirect("User:loader")                                                                                                                  
    else:
        return render(request,"User/Payment.html",{'amt':amt})

def loader(request):
    return render(request,"User/Loader.html")

def paymentsuc(request):
    return render(request,"User/Payment_suc.html")

def mybooking(request):
    book = tbl_booking.objects.filter(user=request.session["uid"],booking_status__gt=0)
    return render(request, "User/mybooking.html",{"book":book})

def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(product=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(product=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    user_name=request.GET.get('user_name')
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session["uid"]),user_review=user_review,rating_data=rating_data,product=tbl_product.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(product=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(product=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(product=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)

def ajaxproduct(request):
    parry=[]
    avg=0
    ar=[1,2,3,4,5]
    if request.GET.get("did") != "" and request.GET.get("search") != "":
        product = tbl_product.objects.filter(category=request.GET.get("did"),product_name__icontains=request.GET.get("search"))
        for i in product:
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

            wishlistcount = tbl_wishlist.objects.filter(user=request.session["uid"],product=i.id).count()
            if wishlistcount > 0:
                i.wishlist = True
            else:
                i.wishlist = False
            tot=0
            ratecount=tbl_rating.objects.filter(product=i.id).count()
            if ratecount>0:
                ratedata=tbl_rating.objects.filter(product=i.id)
                for j in ratedata:
                    tot=tot+j.rating_data
                    avg=tot//ratecount
                    #print(avg)
                parry.append(avg)
            else:
                parry.append(0)
            # print(parry)
        datas=zip(product,parry)
    elif request.GET.get("did") != "":
        product = tbl_product.objects.filter(category=request.GET.get("did"))
        for i in product:
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

            wishlistcount = tbl_wishlist.objects.filter(user=request.session["uid"],product=i.id).count()
            if wishlistcount > 0:
                i.wishlist = True
            else:
                i.wishlist = False
            tot=0
            ratecount=tbl_rating.objects.filter(product=i.id).count()
            if ratecount>0:
                ratedata=tbl_rating.objects.filter(product=i.id)
                for j in ratedata:
                    tot=tot+j.rating_data
                    avg=tot//ratecount
                    #print(avg)
                parry.append(avg)
            else:
                parry.append(0)
            # print(parry)
        datas=zip(product,parry)
    elif request.GET.get("search") != "":
        product = tbl_product.objects.filter(product_name__icontains=request.GET.get("search"))
        for i in product:
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


            wishlistcount = tbl_wishlist.objects.filter(user=request.session["uid"],product=i.id).count()
            if wishlistcount > 0:
                i.wishlist = True
            else:
                i.wishlist = False
            tot=0
            ratecount=tbl_rating.objects.filter(product=i.id).count()
            if ratecount>0:
                ratedata=tbl_rating.objects.filter(product=i.id)
                for j in ratedata:
                    tot=tot+j.rating_data
                    avg=tot//ratecount
                    #print(avg)
                parry.append(avg)
            else:
                parry.append(0)
            # print(parry)
        datas=zip(product,parry)
    else:
        product = tbl_product.objects.all()
        for i in product:
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


            wishlistcount = tbl_wishlist.objects.filter(user=request.session["uid"],product=i.id).count()
            if wishlistcount > 0:
                i.wishlist = True
            else:
                i.wishlist = False
            tot=0
            ratecount=tbl_rating.objects.filter(product=i.id).count()
            if ratecount>0:
                ratedata=tbl_rating.objects.filter(product=i.id)
                for j in ratedata:
                    tot=tot+j.rating_data
                    avg=tot//ratecount
                    #print(avg)
                parry.append(avg)
            else:
                parry.append(0)
            # print(parry)
        datas=zip(product,parry)
    return render(request, 'User/Ajaxproduct.html', {'product': datas,'ar':ar})

def logout(request):
    del request.session["uid"]
    return redirect("Guest:index")

def complaint(request):
    complaint = tbl_complaint.objects.filter(user=request.session["uid"])
    if request.method=="POST":
        tbl_complaint.objects.create(title=request.POST.get("title"),content=request.POST.get("content"),user=tbl_user.objects.get(id=request.session["uid"]))
        return redirect("User:complaint")
    else:
        return render(request,"User/complaint.html",{"complaint":complaint})

def ajaxwishlist(request):
    wishlistcount = tbl_wishlist.objects.filter(user=request.session["uid"],product=request.GET.get("pid")).count()
    if wishlistcount > 0:
        tbl_wishlist.objects.get(user=request.session["uid"],product=request.GET.get("pid")).delete()
        return JsonResponse({"msg":"Removed From Wish List","status":False})
    else:
        tbl_wishlist.objects.create(user=tbl_user.objects.get(id=request.session["uid"]),product=tbl_product.objects.get(id=request.GET.get("pid")))
        return JsonResponse({"msg":"Added To Wish List","status":True})

def mywishlist(request):
    wishlist = tbl_wishlist.objects.filter(user=request.session["uid"])
    for w in wishlist:
        tot=0
        ratecount=tbl_rating.objects.filter(product=w.product.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(product=w.product.id)
            for j in ratedata:
                tot=tot+j.rating_data
                avg=tot//ratecount
            w.avg=avg
        else:
            w.avg=0

        total_stock = tbl_stock.objects.filter(product=w.product.id).aggregate(total=Sum('stock_quantity'))['total']
        total_cart = tbl_cart.objects.filter(product=w.product.id, cart_status=0).aggregate(total=Sum('cart_quantity'))['total']
        if total_stock is None:
            total_stock = 0
        if total_cart is None:
            total_cart = 0
        total =  total_stock - total_cart
        w.total_stock = total
    return render(request,"User/MyWishlist.html",{"wishlist":wishlist})