from django.db import models
from ETF.models import Company

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

# class Domain(models.Model):
#     domain_id = models.IntegerField(primary_key=True)
#     created_at = models.TimeField()
#     updated_at = models.TimeField()
#     domain_name = models.CharField(max_length=100, unique=True)
#
# class Industry(models.Model):
#     industry_id = models.IntegerField(primary_key=True)
#     domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
#     industry_name = models.CharField(max_length=100)
#     created_at = models.TimeField()
#     updated_at = models.TimeField()
#
# class Company(models.Model):
#     company_id = models.IntegerField(primary_key=True)
#     industry_id = models.ForeignKey(Industry, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=100, unique=True)
#     company_size = models.CharField(max_length=50)
#     company_introduction = models.TextField()
#     created_at = models.TimeField()
#     updated_at = models.TimeField()
#
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
