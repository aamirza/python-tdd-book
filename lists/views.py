from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import FormView

from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import Item, List


User = get_user_model()


class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def share(request, list_id):
    list_ = List.objects.get(id=list_id)
    share_with = request.POST.get('sharee', '')
    user_exists = User.objects.filter(email=share_with)
    if user_exists:
        list_.shared_with.add(share_with)
    return redirect(list_)
