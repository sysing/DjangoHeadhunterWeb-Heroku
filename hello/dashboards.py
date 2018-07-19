from controlcenter import Dashboard, widgets
from .models import Candidate
from django.contrib.auth.models import User


class ModelItemList(widgets.ItemList):
    model = Candidate
    list_display = ('id', 'name')

class MySingleBarChart(widgets.SingleBarChart):
    # label and series
    def series(self):
        # Y-axis
        return [1,2,3]

    def labels(self):
        # Duplicates series on x-axis
            return ['Monday','Tuesday','Wednesday']

    def legend(self):
        # Displays labels in legend
        return ['a','b','c']

# class MyChart(widgets.Chart):
#    class Chartist:
#         point_lables = True
#         options = {
#             'reverseData': True,
#         }

class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
        MySingleBarChart,
    )
