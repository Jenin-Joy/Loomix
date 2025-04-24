from django.urls import path
from User import views
app_name="User"

urlpatterns=[
    path('Homepage/',views.home,name='Homepage'),
    path('profile/',views.profile,name='profile'),
    path('Editprofile/',views.editprofile,name='Editprofile'),
    path('Changepassword/',views.changepassword,name='Changepassword'),
    path('viewproduct/',views.viewproduct,name='viewproduct'),#
    path('addcart/<int:pid>',views.addcart,name='addcart'),
    path('Mycart/',views.Mycart, name='Mycart'),  # 
    path("DelCart/<int:did>", views.DelCart,name="delcart"),
    path("CartQty/", views.CartQty,name="cartqty"),
    path("sizeupdate/", views.sizeupdate,name="sizeupdate"),
    path("payment/<int:bid>",views.payment,name="payment"),
    path('loader/',views.loader, name='loader'),
    path('paymentsuc/',views.paymentsuc, name='paymentsuc'),
    path("mybooking/",views.mybooking,name="mybooking"), #

    path('rating/<int:mid>',views.rating,name="rating"),  
    path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
    path('starrating/',views.starrating,name="starrating"),

    path('ajaxproduct/',views.ajaxproduct,name="ajaxproduct"),
    path('logout/',views.logout,name="logout"),
    path('complaint/',views.complaint,name="complaint"),
    
    path('ajaxwishlist/',views.ajaxwishlist,name="ajaxwishlist"),
    
    path('mywishlist/',views.mywishlist,name="mywishlist"),

]


