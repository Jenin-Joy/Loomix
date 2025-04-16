from django.db import models
from Admin.models import*

class tbl_user(models.Model):
    reg_name=models.CharField(max_length=50)
    reg_email=models.CharField(max_length=50)
    reg_address=models.CharField(max_length=50)
    reg_password=models.CharField(max_length=50)
    reg_contact=models.CharField(max_length=50)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_photo=models.FileField(upload_to='Assets/users/photo/')