from django.db import models
from ETF.models import Industry

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
    
    def __str__(self):
        return f"{self.company_name}"

'''
Job {
    job_id      int     pk
    job_name    string  unique
    created_at  time
    updated_at  time
}
'''
class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job_name'], name='unique_job_name')
        ]

    def __str__(self):
        return f"{self.job_name}"


'''
Skill {
    skill_id      int     pk
    skill_name    string  unique
    created_at    time
    updated_at    time
}
'''
class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['skill_name'], name='unique_skill_name')
        ]

    def __str__(self):
        return f"{self.skill_name}"
'''
Recruitment {
    recruitment_id      int     pk      자동생성(ex. 행번호)
    recruitment_title   sting           공고 제목
    url                 string          공고 주소
    created_at          time            레코드 생성 시간
    updated_at          time            레코드 수정 시간
    career              string          요구 경력
    education           string          요구 학력
    due_date            date            마감 기한
    company_id          int     fk      기업 id
    job_id              int     fk      직무 id
    skill_id            int     fk      스킬 id
}
'''
class Recruitment(models.Model):
    recruitment_id = models.AutoField(primary_key=True)
    recruitment_title = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    career = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    due_date = models.DateTimeField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    jobs = models.ManyToManyField(Job, related_name='recruitments')
    skills = models.ManyToManyField(Skill, related_name='recruitments')

    def __str__(self):
        job_names = ",".join([job.job_name for job in self.jobs.all()])
        return f"title: {self.recruitment_title}, jobs: {job_names}"
      
class ProsReview(models.Model):
    pros_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    review_text = models.TextField()

# class ProsWord(models.Model):
#     pros_word_id = models.AutoField(primary_key=True)
#     pros_id = models.ForeignKey(ProsReview, on_delete=models.CASCADE)
#     word_text = models.TextField()
#     word_type = models.BooleanField(default=True, null=False)
#     weight = models.IntegerField(default=0)

class ConsReview(models.Model):
    cons_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    review_text = models.TextField()

# class ConsWord(models.Model):
#     cons_word_id = models.AutoField(primary_key=True)
#     cons_id = models.ForeignKey(ConsReview, on_delete=models.CASCADE)
#     word_text = models.TextField()
#     word_type = models.BooleanField(default=False, null=False)
#     weight = models.IntegerField(default=0)

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    news_title = models.CharField(max_length=255)
    news_text = models.TextField()
    news_url = models.URLField(max_length=512)
    posted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

