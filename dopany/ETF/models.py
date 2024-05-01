# models.py

from django.db import models

'''
Domain {
    domain_id       int         pk
    created_at      time
    updated_at      time
    domain_name     string      unique
}
'''
class Domain(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
