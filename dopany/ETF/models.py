# models.py

from django.db import models

'''
Domain [icon: user, color: blue] {
    domain_id       int         pk
    created_at      time
    updated_at      time
    domain_name     string      unique
    etf_id          string      fk
}
'''

class Domain(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

'''
Etf [icon: user, color: blue] {
    etf_id              int         pk
    created_at          time
    updated_at          time
    transaction_date    time        unique
    closing_price       int
    trading_volume      int
    change              float
    technical_analysis  float
    domain_id           int         fk
}
'''

class Etf(models.Model):
    etf_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_date = models.DateTimeField(unique=True)
    closing_price = models.IntegerField()
    trading_volume = models.IntegerField()
    change = models.FloatField()
    technical_analysis = models.FloatField()
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

