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
Etf  {
    etf_id              int         pk          자동생성(ex. 행번호)
    etf_name	        string                  ETF 상품명(ex. KODEX K-메타버스액티브)
    created_at          time                    레코드 생성 시간
    updated_at          time                    레코드 수정 시간
    transaction_date    time                    거래일
    closing_price       int                     종가
    trading_volume      int                     거래량
    change              float                   변동(%)_전일 종가 대비 당일 종가
    domain_id           int         fk          도메인 id
}
'''
class Etf(models.Model):
    etf_id = models.AutoField(primary_key=True)
    etf_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_date = models.DateTimeField
    closing_price = models.IntegerField()
    trading_volume = models.IntegerField()
    change = models.FloatField()
    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['etf_name', 'transaction_date']
    

'''
EtfMajorCompany {
    eff_major_company_id	int         pk      자동생성(ex. 행번호)
    created_at	            time                레코드 생성 시간
    updated_at	            time                레코드 수정 시간
    company_name	        string              ETF 상품 주요 구성자산 기업이름(ex. CJ ENM)
    etf_name                string      fk      ETF 상품명
}
'''
class EtfMajorCompany(models.Model):
    etf_major_company_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=100, unique=True)
    etf_name = models.ForeignKey(Etf, on_delete=models.CASCADE)