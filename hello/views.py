import sys

from django.http import HttpResponse,QueryDict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import views as auth_views
from django_tables2.config import RequestConfig
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from django.utils.translation import activate
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from .tokens import account_activation_token
from django.core.mail import EmailMessage,send_mail
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, SignUpForm, ProfileForm, CreateJobForm ,SelectJobForm , NameForm
from .models import Candidate, Function, Province , Industry, Education, Profile, Job, Jobs_Candidates
from .tables import CandidateTableMobile, CandidateTableDesktop

import datetime
import pytz
from django.utils import timezone
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


class ActiveUsersJSONView(BaseLineChartView):

    def get_labels(self):
        days = self.request.GET.get('days',5)
        days = int(days)
        res = []
        for x in range (0, days):
            date = datetime.datetime.now() - datetime.timedelta(days = days - x -1)
            # res.append(date.strftime("%a %b %d %H:%M:%S %Z %Y"))
            res.append(date.strftime("%d %b "))
        return res

    def get_providers(self):
        return ["活跃用户",]

    def get_data(self):
        days = self.request.GET.get('days',5)
        days = int(days)
        res = []
        for x in range (0,days):
            # time_min = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) - datetime.timedelta(days= days - x -1) #8hours for UTC+8
            date = datetime.datetime.now() - datetime.timedelta(days = days - x - 1)
            date_str = date.strftime('%Y-%m-%d')
            active_user_count = Profile.objects.filter(last_activity__startswith = date_str).count()
            res.append(active_user_count)
        return [res,]

active_users_json = ActiveUsersJSONView.as_view()

class NewCandidatesJSONView(BaseLineChartView):

    def get_labels(self):
        res = []
        days = 5
        for x in range (0,days):
            date = datetime.datetime.now() - datetime.timedelta(days = days - x - 1)
            res.append(date.strftime("%d %b "))
        return res

    def get_providers(self):
        return ["新增候选人",]

    def get_data(self):
        res = []
        days = 5
        for x in range (0,days):
            time_min = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) - datetime.timedelta(days= days - x -1) #8hours for UTC+8
            time_max = time_min + datetime.timedelta(days=1)
            new_candidates_count = Candidate.objects.filter(ctime__gt = time_min,ctime__lt = time_max).count()
            res.append(new_candidates_count)
        return [res,]

new_candidates_json = NewCandidatesJSONView.as_view()

class TopCandidatesJSONView(BaseLineChartView   ):
    candidates_jobs = Jobs_Candidates.objects.all()
    job_count = {}
    for c in candidates_jobs:
        if not  c.candidate_id in job_count:
            job_count[c.candidate_id] = 1
        else:
            job_count[c.candidate_id] = job_count[c.candidate_id] + 1
    sorted_keys = sorted(job_count, key=job_count.get,  reverse=True)[:5]

    def get_labels(self):
        label = []
        for value in self.sorted_keys:
            candidate = Candidate.objects.get(id = value)
            label_name = candidate.__str__()
            label.append(label_name)
        return label

    def get_providers(self):
        return ["候选人岗位数",]

    def get_data(self):
        data = []
        for k in self.sorted_keys:
            data.append(self.job_count[k])
        return [data,]

top_candidates_json = TopCandidatesJSONView.as_view()

class TopFunctionsJSONView(BaseLineChartView):
    candidates_jobs = Jobs_Candidates.objects.all()
    function_count = {}
    for c in candidates_jobs:
        function = c.candidate.function
        if not  function.name in function_count:
            function_count[function.name] = 1
        else:
            function_count[function.name] = function_count[function.name] + 1
    sorted_keys = sorted(function_count, key=function_count.get,  reverse=True)[:5]

    def get_labels(self):
        return self.sorted_keys

    def get_providers(self):
        return ["职能岗位申请",]

    def get_data(self):
        data = []
        for k in self.sorted_keys:
            data.append(self.function_count[k])
        return [data,]

top_functions_json = TopFunctionsJSONView.as_view()


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart_json = LineChartJSONView.as_view()

def dashboard(request):
    context = {}
    context['form'] = NameForm()
    return render(request,'dashboard/dashboard.html',context)

def index(request):
    # profile = Profile.objects.get(user=request.user)
    # return HttpResponse(profile.last_activity)
    # CandidateFactory.create()
    context = {}
    context['criterias'] = []
    context['criterias'].append(Province.objects.all())
    context['criterias'].append(Function.objects.all())
    context['criterias'].append(Industry.objects.all())
    context['criterias'].append(Education.objects.all())
    special_params = ['page','sort','rm','search']
    fields = [(f.name) for f in Candidate._meta.get_fields()]
    context['search_bar'] = True
    context['filters'] = {}
    candidate = Candidate.objects.all().order_by('-ctime')

    for key,vals in request.GET.lists():
        if (key.split('__')[0] in fields): #get field.name , ie 'province' from 'province_code'
            field_name = key.split('__')[0]
            field_verbose_name = Candidate._meta.get_field(field_name).verbose_name
            class_ins =  getattr(sys.modules[__name__], field_name.title())
            obj_name = class_ins.objects.get(id = vals[0]).name
            filter_label = field_verbose_name + ' : ' + obj_name
            context['filters'][key] = filter_label
            candidate = candidate.filter(**{key: vals[0]})
        elif(key == 'search'):
            candidate = candidate.filter(
            Q(index__icontains=vals[0]) |
            Q(name__icontains=vals[0]) |
            Q(role__icontains=vals[0]) |
            Q(companies__icontains=vals[0])|
            Q(remarks__icontains=vals[0])|
            Q(province__name__icontains=vals[0])|
            Q(industry__name__icontains=vals[0])|
            Q(function__name__icontains=vals[0])
            )
            context['filters']['search'] = '搜索 : ' + vals[0]
        elif (key == 'rm'): #remove get params
            querydict = request.GET.copy()
            querydict.pop('rm')
            if  querydict.__contains__(vals[0]):
                querydict.pop(vals[0])
            return redirect('/?{}'.format(querydict.urlencode()))
                    # for criteria in context['criterias']:
                    # candidates = criteria.filter(code__icontains=vals[0])
                    # candidates.extend = criteria.filter(name__icontains=vals[0])
    context['candidate'] = candidate
    context['get_dict'] = request.GET.dict()
    if  request.user_agent.is_mobile: # returns True
        table = CandidateTableMobile(candidate)
    else:
        table = CandidateTableDesktop(candidate)
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    context['table'] = table
    return render(request,'listing/home.html',context)

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('成功更新账号信息'))
            return redirect('index')
        else:
            messages.error(request, _('请纠正以下资料'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,'profile/update_profile.html', {'profile_form': profile_form})

def login(request, template_name='registration/login.html', redirect_field_name = None, authentication_form = LoginForm, extra_context=None):
    return auth_views.login(request, template_name, redirect_field_name, authentication_form)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.company_name = form.cleaned_data.get('company_name')
            user.profile.company_description = form.cleaned_data.get('company_description')
            user.profile.company_address = form.cleaned_data.get('company_address')
            user.profile.company_size = form.cleaned_data.get('company_size')
            user.profile.wechat_id = form.cleaned_data.get('wechat_id')
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.add_message(request, messages.INFO, "账号创建成功，请登录。查询候选人资料需要管理员认证账号")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def candidate_select_job(request,pk):

    if request.user.is_anonymous:
        messages.warning(request, _('请登录已验证账号'))
        return redirect('login')
    if not request.user.profile.is_verified:
        messages.warning(request, _('查询候选人需要管理员验证账号资料'))
        return redirect('update_profile')

    if request.method == 'POST':
        form = SelectJobForm(request.POST, user=request.user)
        if form.is_valid():
            candidate = Candidate.objects.get(id=pk)
            job = form.cleaned_data['job']
            new_jc = Jobs_Candidates.objects.filter(job_id = job.id  , candidate_id = candidate.id)[:1]
            if new_jc:
                messages.warning(request, _('您之前已为选人(%s)添加过岗位(%s)' %(candidate.index ,job.title)))
                return redirect('index')
                return HttpResponse(new_jc)
            else:
                new_jc = Jobs_Candidates(job = job, candidate = candidate )
                new_jc.save()
                messages.success(request, _('成功为候选人(%s)添加岗位(%s)信息' %(candidate.index ,job.title)))
                return redirect('index')
    else:
        form = SelectJobForm(user=request.user)
    return render(request, 'form/select_job.html', {'job_form':form,'pk': pk})

def candidate_create_job(request,pk):

    if request.user.is_anonymous:
        messages.warning(request, _('请登录已验证账号'))
        return redirect('login')
    if not request.user.profile.is_verified:
        messages.warning(request, _('请填写公司资料便管理员认证'))
        return redirect('update_profile')

    if request.method == 'POST':
        form = CreateJobForm(request.POST)
        if form.is_valid():
            candidate = Candidate.objects.get(id=pk)
            job = form.save(commit=False)
            # job.refresh_from_db()  # load the profile instance created by the signal
            job.recruiter = request.user
            job.save()
            jobs_candidates = Jobs_Candidates(job = job, candidate = candidate)
            jobs_candidates.save()
            messages.success(request, _('成功为候选人(%s)添加岗位(%s)信息' %(candidate.index ,job.title)))
            return redirect('index')
    else:
        form = CreateJobForm()
    return render(request, 'form/create_job.html', {'job_form':form})



def language(request, language = 'en-gb'):

    response = HttpResponse("setting language to %s" % language)
    response.set_cookie('lang',language)
    request.session['lang'] = language
    return response;

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# from django.shortcuts import render
# from django.http import HttpResponse
#
# from .models import Greeting
#
# import requests
# import os
# # Create your views here.
# def index(request):
#     # return HttpResponse('Hello from Python!')
#     # return render(request, 'index.html')
#     times = int(os.environ.get('TIMES',3))
#     return HttpResponse('Hello!'* times)
#     requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     return HttpResponse('<pre>' + r.text + '</pre>')
#
#
# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})
