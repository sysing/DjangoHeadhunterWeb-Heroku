from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Job
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape,format_html
import urllib

def mark_compulsory(label):
    return "<span style = 'font-weight:bold'>"+label+"*</span>"

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.placeholder = 'Username'
        self.fields['password'].widget.placeholder = 'Password'

class SignUpForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    error_messages = {
        'password_mismatch': ("密码不一致！"),
    }
    username = forms.CharField(label = format_html(mark_compulsory('登录名')))
    password1 = forms.CharField(label=format_html(mark_compulsory("密码")), widget=forms.PasswordInput)
    password2 = forms.CharField(label=format_html(mark_compulsory("密码确认")), widget=forms.PasswordInput)
    company_name = forms.CharField(max_length = 20, label = format_html(mark_compulsory('公司名称')))
    company_description = forms.CharField(widget=forms.Textarea, label = format_html(mark_compulsory('公司简介')))
    company_address = forms.CharField(max_length = 50, label ='公司地址', required = False)
    company_size = forms.CharField(max_length = 20, label ='公司人员规模', required = False)
    wechat_id = forms.CharField(max_length = 20, label = '微信号', required = False)
    bio = forms.CharField(widget=forms.Textarea, label ='个人简介', required = False)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user

class ProfileForm(forms.ModelForm):
    company_name = forms.CharField(max_length = 20, label = format_html(mark_compulsory('公司名称')))
    company_description = forms.CharField(widget=forms.Textarea, label = format_html(mark_compulsory('公司简介')))
    class Meta:
        model = Profile
        exclude = ('user','is_verified')

class CreateJobForm(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ('recruiter','candidates')

class SelectJobForm(forms.Form):
    job = forms.ModelChoiceField(queryset=Job.objects.none(), label='选择岗位')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SelectJobForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['job'].queryset = Job.objects.filter(recruiter= user)

class NameForm(forms.Form):
    name = forms.CharField

    def as_url_args(self):
        if self.is_valid():
            return urllib.parse.urlencode(self.cleaned_data)
