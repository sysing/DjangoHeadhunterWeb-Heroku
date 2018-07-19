import factory
from .models import Candidate
class CandidateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Candidate

    index = factory.Sequence(lambda n: 'C{00000000}'.format(n))
    name = 'Name'
    role= 'Role'
    industry_id = 1
    function_id = 1
    @factory.Sequence
    def sex_id(n):
        if n % 2 == 0 :
            return '1'
        else:
            return '2'
    age = 25
    education_id = factory.Iterator([1,2,3])
    companies = 'Companies'
    funding = 'Funding'
    province_id = 1
    current_salary = 'current_salary'
    expected_salary = 'expected_salary'
    remarks = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    # ctime = models.DateTimeField(auto_now_add = True, verbose_name ='创建时间')
    # mtime = models.DateTimeField(auto_now = True, verbose_name ='更新时间')
    resume_link = 'www.link.com'
    # ctime = factory.LazyAttribute(lambda o : datetime.utcnow())
    # mtime = factory.LazyAttribute(lambda o : o.now + datetime.timedelta(days=4))
# Another, different, factory for the same object
