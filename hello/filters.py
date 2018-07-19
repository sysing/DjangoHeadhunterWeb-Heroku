import django_filters
from .models import Candidate

class CandidateFilter(django_filters.FilterSet):
    class Meta:
        model = Candidate
        fields = {
            'age':['lt','gt'],
        }
