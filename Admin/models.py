from django.db import models

# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)

class tbl_category(models.Model):
    category_name=models.CharField(max_length=50)

class tbl_adminreg(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=50)
class tbl_brand(models.Model):
    brand_name=models.CharField(max_length=50)

class tbl_place(models.Model):
    place_name=models.CharField(max_length=50)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=30)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)

class tbl_size(models.Model):
    size_name=models.CharField(max_length=50)

class tbl_product(models.Model):
    product_name = models.CharField(max_length=100)
    product_photo = models.FileField(upload_to='assets/product/photo')
    product_price = models.CharField(max_length=100)
    product_total_price=models.CharField(max_length=100)
    product_description=models.CharField(max_length=100,null=True)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)

class tbl_productsize(models.Model):
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
    size=models.ForeignKey(tbl_size,on_delete=models.CASCADE)

class tbl_stock(models.Model):
    stock_date=models.DateField(auto_now_add=True)
    stock_quantity=models.CharField(max_length=50)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)


