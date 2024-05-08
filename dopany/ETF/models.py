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
EtfProduct  {
    etf_product_id      int         pk          자동생성(ex. 행번호)
    etf_product_name	string      unique      ETF 상품명(ex. KODEX K-메타버스액티브)
    created_at          time                    레코드 생성 시간
    updated_at          time                    레코드 수정 시간
    domain_id           int         fk          도메인 id
}
'''
class EtfProduct(models.Model):
    etf_product_id = models.AutoField(primary_key=True)
    etf_product_name = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    

'''
EtfPrice  {
    etf_price_id        int         pk          자동생성(ex. 행번호)
    created_at          time                    레코드 생성 시간
    updated_at          time                    레코드 수정 시간
    transaction_date    time                    거래일
    closing_price       int                     종가
    trading_volume      int                     거래량
    change              float                   변동(%)_전일 종가 대비 당일 종가
    etf_product_id      int         fk          etf 상품 id
}
'''
class EtfPrice(models.Model):
    etf_price_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_date = models.DateTimeField(null=False)
    closing_price = models.IntegerField()
    trading_volume = models.IntegerField()
    change = models.FloatField()
    etf_product = models.ForeignKey(EtfProduct, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['etf_product', 'transaction_date'], name='unique_etf_product_transaction_date')
        ]
 


'''
EtfMajorCompany {
    etf_major_company_id	int         pk      자동생성(ex. 행번호)
    created_at	            time                레코드 생성 시간
    updated_at	            time                레코드 수정 시간
    company_name	        string              ETF 상품 주요 구성자산 기업이름(ex. CJ ENM)
    etf_product_id          int         fk      
}
'''
class EtfMajorCompany(models.Model):
    etf_major_company_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=100)
    etf_product = models.ForeignKey(EtfProduct, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['etf_product', 'company_name'], name='unique_etf_product_company_name')
        ]
    
    
    
'''
Industry {
    industry_id	    int         PK	        자동생성(ex. 행번호)
    created_at		time                    레코드 생성 시간
    updated_at		time                    레코드 수정 시간
    industry_name	string      unique    	산업 이름(ex. IT.정보통신업>게임.애니메이션)
    domain_id	    int         FK	        도메인 id
}
'''
class Industry(models.Model):
    industry_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    industry_name = models.CharField(max_length=255, unique=True)
    domains = models.ManyToManyField(Domain, related_name='industries')


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
    company_addr            string                  기업 주소
    industry_id             int         FK          산업 id
}
'''
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
