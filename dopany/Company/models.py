from django.db import models

class Domain(models.Model):
    domain_id = models.IntegerField(primary_key=True)
    created_at = models.TimeField()
    updated_at = models.TimeField()
    domain_name = models.CharField(max_length=100, unique=True)
    
class Industry(models.Model):
    industry_id = models.IntegerField(primary_key=True)
    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    industry_name = models.CharField(max_length=100)
    created_at = models.TimeField()
    updated_at = models.TimeField()
    
class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    industry_id = models.ForeignKey(Industry, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, unique=True)
    company_size = models.CharField(max_length=50)
    company_introduction = models.TextField()
    created_at = models.TimeField()
    updated_at = models.TimeField()

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
    stock_id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.TimeField()
    updated_at = models.TimeField()
    transaction_date = models.TimeField(unique=True)
    closing_price = models.IntegerField()
    trading_volume = models.IntegerField()
    change = models.FloatField()
