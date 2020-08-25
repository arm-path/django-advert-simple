from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# pip install python-slugify (Преобразование строки в slug)
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from slugify import slugify

from main_app.utils import AccessToEditAndDeleteDataMixin
from .models import Gallery, Image
from .forms import GalleryForm, ImageForm


class GalleryListView(ListView):
    """Список галлереи пользователя системы"""
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'galleries'
    paginate_by = 1

    def get_queryset(self):
        """Фильтрация галлереи по пользователю системы"""
        return Gallery.objects.filter(user=self.request.user)


class GalleryDetailView(LoginRequiredMixin, DetailView):
    """Галерея"""
    model = Gallery
    context_object_name = 'gallery'
    template_name = 'gallery/gallery_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Галерея: ' + str(self.object.title)
        # Pagination image model
        images = Image.objects.filter(gallery=self.object)
        context['paginator'] = Paginator(images, 3)
        page_number = self.request.GET.get('page')
        context['page_obj'] = context['paginator'].get_page(page_number)
        context['is_paginated'] = context['page_obj'].has_other_pages()

        return context


class GalleryCreate(LoginRequiredMixin, CreateView):
    """Создание галереи"""
    model = Gallery
    form_class = GalleryForm
    template_name = 'gallery/gallery_form.html'

    def get_context_data(self, *args, **kwargs):
        """Передача дополнительных данных в шаблон"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление галереи'
        return context

    def post(self, request, *args, **kwargs):
        """Переопределение метода post, для определения поля user перед сохранением"""
        form = self.form_class(request.POST)
        form_post = form.save(commit=False)
        form_post.user = request.user
        form_post.slug = slugify(form_post.title)
        form_post.save()
        return redirect('gallery_detail', form_post.slug)


class GalleryUpdate(AccessToEditAndDeleteDataMixin, UpdateView):
    """Обновление, редактирование галереии"""
    model = Gallery
    form_class = GalleryForm
    template_name = 'gallery/gallery_form.html'

    def form_valid(self, form):
        """Переопределение метода post, для переопределения поля slug перед сохранением"""
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title)
        self.object.save()
        return super().form_valid(form)


class GalleryDelete(AccessToEditAndDeleteDataMixin, DeleteView):
    """Удаление галереии"""
    model = Gallery
    success_url = reverse_lazy('gallery_list')


class ImageCreate(AccessToEditAndDeleteDataMixin, CreateView):
    """Создание изображения"""
    model = Image
    template_name = 'gallery/gallery_form.html'
    form_class = ImageForm

    def get_context_data(self, *args, **kwargs):
        """Передача дополнительных данных в шаблон"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление изображения'
        return context

    def get(self, request, *args, **kwargs):
        """Система защиты от изменения url адреса галереии на url адрес галереии другого пользователя"""
        gallery_user = Gallery.objects.get(slug=self.kwargs['slug'])
        if request.user == gallery_user.user:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied  # Ошибка 403, Отказано в доступе

    def post(self, request, *args, **kwargs):
        """Обработка POST Запроса, добавление изображения, добавление поля user и gallery"""
        form = ImageForm(request.POST, files=request.FILES)
        # files=request.FILES - Изображение
        # Не забыть в форме добавить enctype="multipart/form-data"
        if form.is_valid():
            gallery_user = Gallery.objects.get(slug=self.kwargs['slug'])
            post = form.save(commit=False)
            post.user = request.user
            post.gallery = gallery_user
            post.save()
        else:
            pass
        return redirect('gallery_detail', self.kwargs['slug'])


class ImageDelete(AccessToEditAndDeleteDataMixin, DeleteView):
    """Удаление изображения"""
    model = Image

    def get_success_url(self):
        return reverse_lazy('gallery_detail', kwargs={'slug': self.kwargs['gallery']})
