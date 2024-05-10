from django.db import models
from ETF.models import Industry

class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, unique=True)
    company_size = models.CharField(max_length=255)
    company_introduction = models.TextField()
    company_sales = models.CharField(max_length=255)
    company_url = models.URLField()
    company_img_url = models.URLField()
    company_addr = models.CharField(max_length=255)
    industries = models.ManyToManyField(Industry, related_name='companies')

class ProsReview(models.Model):
    pros_id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    review_text = models.TextField()

class ProsWord(models.Model):
    pros_word_id = models.IntegerField(primary_key=True)
    pros_id = models.ForeignKey(ProsReview, on_delete=models.CASCADE)
    word_text = models.TextField()
    word_type = models.BooleanField(default=True, null=False)
    weight = models.IntegerField(default=0)

class ConsReview(models.Model):
    cons_id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    review_text = models.TextField()

class ConsWord(models.Model):
    cons_word_id = models.IntegerField(primary_key=True)
    cons_id = models.ForeignKey(ConsReview, on_delete=models.CASCADE)
    word_text = models.TextField()
    word_type = models.BooleanField(default=False, null=False)
    weight = models.IntegerField(default=0)

class News(models.Model):
    news_id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    news_title = models.CharField(max_length=100)
    news_text = models.TextField()
    created_at = models.TimeField()
    updated_at = models.TimeField()

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_date = models.DateTimeField(null=False)
    closing_price = models.IntegerField()
    trading_volume = models.IntegerField()
    change = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'transaction_date'], name='unique_company_transaction_date')
        ]

