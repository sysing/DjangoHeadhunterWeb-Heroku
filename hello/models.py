from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
from django.db import models


class Candidate(models.Model):
    index = models.CharField(max_length = 9, verbose_name ='编号', unique = True)
    name = models.CharField(max_length = 30, verbose_name = '姓名')
    role= models.CharField(max_length = 20, verbose_name = '期望职位')
    industry = models.ForeignKey('Industry', on_delete = models.SET_NULL, null=True, verbose_name = '行业')
    function = models.ForeignKey('Function', on_delete = models.SET_NULL, null=True, verbose_name = '职能')
    function_multi = models.ManyToManyField('Function',related_name='function_multi')
    province = models.ForeignKey('Province', on_delete=models.SET_NULL, null=True, verbose_name ='城市')
    education = models.ForeignKey('Education', default = 1, on_delete = models.SET_NULL, null=True, verbose_name = '学历')
    age = models.PositiveSmallIntegerField(default = '30', verbose_name ='年龄')
    companies = models.CharField(max_length = 100, blank = True, verbose_name = '曾就职公司')
    funding = models.CharField(max_length = 20, blank = True, verbose_name ='期望轮次')
    current_salary = models.CharField(max_length =20, blank = True, verbose_name ='目前薪资' )
    expected_salary = models.CharField(max_length = 30, blank = True, verbose_name ='期望薪资')
    remarks = models.TextField(max_length = 100, blank = True, verbose_name ='推荐人评语')
    ctime = models.DateTimeField(auto_now_add = True, verbose_name ='创建时间')
    mtime = models.DateTimeField(auto_now = True, verbose_name ='更新时间')
    resume_link = models.URLField(blank = True, verbose_name = '简历链接')
    status = models.ForeignKey('Candidate_Status', on_delete = models.SET_NULL,  null=True, verbose_name = '状态')
    sex = models.ForeignKey('Sex', on_delete = models.SET_NULL, null=True, verbose_name ='性别')
    def __str__(self):
        return self.index+' : '+self.name

    @property
    def intro(self):
        return "<span class='font-weight-bold'>{}</span> <br/> {}  {}岁 <br/>{} {}<br/> <br/><span class='font-weight-bold'>{} </span><br/>{}<br/> {}".format(self.index, self.sex, self.age, self.education, self.province, self.role, self.industry, self.function)

    @property
    def expectations(self):
        string = ""
        if self.companies:
            string += "<span>曾就职：<br/>{}</span> <br/> <br/>".format(self.companies)
        if self.current_salary:
            string += "<span>目前薪资：{}</span> <br/>".format(self.current_salary)
        if self.expected_salary:
            string += "<span>期望薪资：{}</span><br/>".format(self.expected_salary)
        if self.funding:
            string += "<span>期望{}公司</span> ".format(self.funding)
        return string
    def table_mtime(self):
        return self.mtime.strftime("%a %b %d %H:%M:%S %Z %Y")

class Criteria(models.Model):
    def get_filter_id(self):
        return self.__class__.__name__.lower() + '__id'
    class Meta:
        abstract = True

class Candidate_Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Function(Criteria):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_chinese_label(self):
        return '职能'

class Industry(Criteria):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_chinese_label(self):
        return '行业'

class Province(Criteria):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_chinese_label(self):
        return '城市'

class Education(Criteria):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get_chinese_label(self):
        return '学历'

class Sex(Criteria):
    name = models.CharField(max_length=1)

    def __str__(self):
        return self.name

    def get__chinese_label(self):
        return '性别'


class Job(models.Model):
    DELETED = 0
    ACTIVE = 1
    CLOSED = 2
    title = models.CharField(max_length = 20, verbose_name = '职位名称')
    supervisor = models.CharField(max_length = 20, verbose_name = '汇报线')
    salary = models.CharField(max_length = 50, verbose_name = '薪资范围' )
    description = models.TextField(verbose_name = '职位描述' )
    recruiter = models.ForeignKey( User, on_delete = models.SET_NULL, null=True, verbose_name = '招聘者')
    status = models.PositiveSmallIntegerField(verbose_name = '状态', default = ACTIVE)

    def __str__(self):
        return self.recruiter.profile.company_name + ' : ' + self.title

class Jobs_Candidates(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length = 20, verbose_name = '公司名称')
    company_description = models.TextField(verbose_name = '公司介绍')
    company_address = models.CharField(max_length = 50, blank = True, verbose_name = '公司地址')
    company_size = models.CharField(max_length = 20, blank = True, verbose_name = '公司人员规模')
    wechat_id = models.CharField(max_length = 20, blank = True, verbose_name = '微信号')
    bio = models.TextField(max_length=500, blank=True, verbose_name = '自我介绍')
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default = False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username
