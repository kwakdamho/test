from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountCreationForm
from accountapp.models import HelloWorld




@login_required
def hello_world(request):

    if request.user.is_authenticated:
        if request.method == 'POST':

            temp = request.POST.get('input')

            new_data = HelloWorld()
            new_data.text = temp
            new_data.save()

            return HttpResponseRedirect(reverse('accountapp:hello_world'))
        else:
            data_list = HelloWorld.objects.all()
            return render(request, 'accountapp/hello_world.html',
                          context={'data_list': data_list})
    else:
        return HttpResponseRedirect(reverse('accountapp:login'))


class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'


has_ownership_required = [login_required, account_ownership_required]


@method_decorator(has_ownership_required, 'get')
@method_decorator(has_ownership_required, 'post')
class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountCreationForm
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'


@method_decorator(has_ownership_required, 'get')
@method_decorator(has_ownership_required, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/delete.html'

