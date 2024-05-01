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



'''
Industry {
    industry_id	    int         PK	    자동생성(ex. 행번호)
    created_at		time                레코드 생성 시간
    updated_at		time                레코드 수정 시간
    industry_name	string          	산업 이름(ex. IT.정보통신업>게임.애니메이션)
    domain_name	    string      FK	    도메인 이름

    industry_name + domain_name	unique,복합키	
}
'''
class Industry(models.Model):
    industry_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    industry_name = models.CharField(max_length=255)
    domain_name = models.ForeignKey(Domain, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['industry_name', 'domain_name']


'''
Company {
    company_id	            int         PK	        자동생성(ex. 행번호)
    created_at		        time                    레코드 생성 시간
    updated_at		        time                    레코드 수정 시간
    company_name	        string      unique	    기업명
    company_size		    string                  기업 규모(ex. 대기업, 중소기업)
    company_introduction	string              	기업 설명
    company_sales		    string                  매출액
    company_url		        url                     기업 사이트 url
    company_img_url		    url                     기업 사진 url
}
'''
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=255, unique=True)
    company_size = models.CharField(max_length=255)
    company_introduction = models.TextField()
    company_sales = models.CharField(max_length=255)
    company_url = models.URLField()
    company_img_url = models.URLField()
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
