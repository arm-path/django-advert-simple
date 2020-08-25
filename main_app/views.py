from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
# pip install python-slugify (Преобразование строки в slug)
from slugify import slugify

from gallery_app.models import Image, models
from .models import Advert
from .utils import AccessToEditAndDeleteDataMixin
from .forms import AdvertForm


class AdvertListView(ListView):
    """Список объявлений"""
    model = Advert
    template_name = 'main_app/advert_list.html'
    context_object_name = 'adverts'
    paginate_by = 2


class AdvertListViewUser(LoginRequiredMixin, ListView):
    """Список объявлений пользователя"""
    template_name = 'main_app/advert_list.html'
    context_object_name = 'adverts'
    paginate_by = 2

    def get_queryset(self):
        return Advert.objects.filter(user=self.request.user)


class AdvertSearch(ListView):
    """Поиск объявлений"""
    models = Advert
    template_name = 'main_app/advert_list.html'
    context_object_name = 'adverts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        """Переопределение pagination, построение ссылки вида ?search=ТЕКСТ_ПОИСКА&page=1"""
        context = super().get_context_data(*kwargs)
        context['search'] = context[
            'search'] = f'search={ self.request.GET.get("search") }&'
        context['search_list'] = True
        return context

    def get_queryset(self):
        return Advert.objects.filter(title__icontains=self.request.GET.get('search'))


class AdvertDetailView(LoginRequiredMixin, DetailView):
    """Объявление"""
    model = Advert
    template_name = 'main_app/advert_detail.html'
    context_object_name = 'advert'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Image.objects.filter(gallery=self.object.gallery)
        context['access'] = AccessToEditAndDeleteDataMixin.userVerification(
            self)
        return context


class AdvertCreate(LoginRequiredMixin, CreateView):
    """Создание объявления"""
    model = Advert
    template_name = 'main_app/advert_form.html'

    def get_context_data(self, *args, **kwargs):
        """Передача дополнительных данных в шаблон"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление объявления'
        return context

    def get_form(self, form_class=AdvertForm):
        """ 
            Переопределение метода get_form
            При инициализации формы, передача в форму пользователя системы, 
            для построения списка галлереии. См. froms.py
        """
        form = AdvertForm(user_gallery=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        """Переопределение метода post, для определения поля user перед сохранением"""
        form = AdvertForm(request.user, request.POST)
        post = form.save(commit=False)
        post.user = request.user
        post.slug = slugify(post.title)
        post.save()
        return redirect('advert_detail', post.slug)


class AdvertUpdate(AccessToEditAndDeleteDataMixin, UpdateView):
    """Обновление объявления"""
    model = Advert
    form_class = AdvertForm
    template_name = 'main_app/advert_form.html'

    def get_context_data(self, *args, **kwargs):
        """Передача дополнительных данных в шаблон"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование объявления'
        return context

    def form_valid(self, form):
        """Переопределение метода post, для переопределения поля slug перед сохранением"""
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title)
        self.object.save()
        return super().form_valid(form)


class AdvertDelete(AccessToEditAndDeleteDataMixin, DeleteView):
    """Удаления объявления"""
    model = Advert
    success_url = reverse_lazy('advert_list')
