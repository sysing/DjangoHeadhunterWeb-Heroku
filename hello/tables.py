import django_tables2 as tables
from .models import Candidate
from django_tables2.views import SingleTableMixin
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django_tables2.utils import Accessor as A

class EditLink(tables.Column):
    empty_values = list()
    def render(self, value, record):
        return mark_safe('<button id="%s" class="btn btn-info">查询</button>' % escape(record.id))

class CandidateTableMobile(tables.Table):
    intro = tables.Column(attrs = {'th':{'style': 'min-width:150px',}},verbose_name ='候选人')
    expectations = tables.Column(attrs = {'th':{'style': 'min-width:200px',}},verbose_name ='')
    remarks = tables.Column(attrs = {'th':{'style': 'min-width:350px',}})

    class Meta:
        model = Candidate
        row_attrs = {
            'class':'clickable-row',
            'data-href':'',
            'onclick': lambda record: "window.location='/candidate_select_job/"+ str(record.pk) + "'" ,
        }
        orderable = False
        sequence = ( 'intro','expectations')
        # exclude = ('index','age','function','industry','role','current_salary','province','education','id','name','resume_link','ctime','status')
        fields = ()
        attrs = {'class': 'table'}

    def render_intro(self,value):
        return mark_safe(value)

    def render_cv(self,value):
        return mark_safe(value)

    def render_expectations(self,value):
        return mark_safe(value)

class CandidateTableDesktop(tables.Table):

    class Meta:
        model = Candidate
        row_attrs = {
            'class':'clickable-row',
            'data-href':'',
            'onclick': lambda record: "window.location='/candidate_select_job/"+ str(record.pk) + "'" ,
        }
        orderable = False
        # exclude = ('index','age','function','industry','role','current_salary','province','education','id','name','resume_link','ctime','status')
        fields = ('index','name','age','education','province','role','industry','function','companies','current_salary','expected_salary','remarks')
        attrs = {'class': 'table'}

    def render_intro(self,value):
        return mark_safe(value)

    def render_cv(self,value):
        return mark_safe(value)

    def render_expectations(self,value):
        return mark_safe(value)
