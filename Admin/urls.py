from django.contrib import admin
from django.urls import path,include
from Admin import views
app_name="Admin"


urlpatterns = [
  path('homepage/',views.homepage,name='homepage'),
  path('add/',views.add,name='add'),
  path('Largest/',views.Largest,name='Largest'),
  path('Calulator/',views.Calculator,name='Calulator'),
  path('district/',views.District,name='district'),
  path('Category/',views.Category,name='Category'),
  path('AdminReg/',views.adminreg,name='adminreg'), 
  path('deladmin/<int:id>',views.deladmin,name='deladmin'), 
  path('deldis/<int:id>',views.deldis,name='deldis'), 
  path('place/',views.place,name='place'),
  path('delplace/<int:id>',views.delplace,name='delplace'),
  path('editplace/<int:id>',views.editplace,name='editplace'),
  path('brand/',views.brand,name="brand"),
  path('bdelete/<int:id>',views.bdelete,name='bdelete'),
  path('bedit/<int:id>',views.bedit,name='bedit'),
  path('subcategory/',views.subcategory,name="subcategory"),
  path('cdelete/<int:id>',views.cdelete,name='cdelete'),
  path('cedit/<int:id>',views.cedit,name='cedit'),
  path('product/',views.product,name='product'),
  path('size/',views.size,name='size'),
  path('deletesize/<int:id>',views.deletesize,name='deletesize'),
  path('addsize/<int:id>',views.addsize,name='addsize'),
  path('deleteaddsize/<int:id>/<int:sizeid>',views.deleteaddsize,name='deleteaddsize'),
  path('Stock/<int:id>',views.Stock,name='Stock'),
  path('delstock/<int:did>',views.delstock,name='delstock'),
  path('logout/',views.logout,name='logout'),
  path('viewbooking/',views.viewbooking,name='viewbooking'),
  path('viewcomplaint/',views.viewcomplaint,name='viewcomplaint'),
  path('reply/<int:id>',views.reply,name='reply'),
  

  
]