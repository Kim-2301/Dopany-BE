from django.contrib import admin
from .models import *
from ETF.models import Domain, Industry

# Register your models here.
admin.site.register(Domain)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(ProsReview)
admin.site.register(ConsReview)
admin.site.register(ProsWord)
admin.site.register(ConsWord)
admin.site.register(News)
admin.site.register(Stock)
admin.site.register(Recruitment)
admin.site.register(Job)
admin.site.register(Skill)
