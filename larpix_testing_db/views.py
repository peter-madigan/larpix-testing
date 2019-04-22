from django.views import View
from django.views.generic import CreateView, ListView
from .models import ASIC

class Home(View):
    pass

class ASICListView(ListView):
    model = ASIC
    paginate_by = 100

class ASICCreateView(CreateView):
    model = ASIC
    fields = ('version', 'packaged', 'status', 'test_results', 'note')
