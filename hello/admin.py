from django.contrib import admin

# Register your models here.
from .models import Function, Candidate, Industry, Province, Education, Profile, Job, Jobs_Candidates, Candidate_Status

admin.site.register(Candidate)
admin.site.register(Jobs_Candidates)
admin.site.register(Function)
admin.site.register(Industry)
admin.site.register(Province)
admin.site.register(Education)
admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Candidate_Status)
