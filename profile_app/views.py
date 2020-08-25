from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, UpdateView
from django.core.exceptions import PermissionDenied

from main_app.utils import AccessToEditAndDeleteDataMixin
from .models import Profile, get_photo_path
from .forms import ProfileForm


class ProfileDetailView(DetailView):
    """Профиль"""
    model = Profile
    template_name = 'profile_app/profile_detail.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        """Система защиты от изменения url адреса профиля на url адрес профиля другого пользователя"""
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object.user != request.user:
            raise PermissionDenied
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль пользователя'
        return context


class ProfileUpdate(AccessToEditAndDeleteDataMixin, UpdateView):
    """Обновление профиля"""
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_app/profile_form.html'

    def get_context_data(self, *args, **kwargs):
        """Передача дополнительных данных в шаблон"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context

    def get(self, request, *args, **kwargs):
        """Система защиты от изменения url адреса профиля на url адрес профиля другого пользователя"""
        self.object = self.get_object()
        if self.object.user != request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        """Обработка POST Запроса, добавление изображения"""
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            telephone_number = form.cleaned_data['telephone_number']
            photo = form.cleaned_data['photo']
            Profile.objects.update_or_create(user=request.user, defaults={
                'first_name': first_name, 'last_name': last_name, 'telephone_number': telephone_number, 'photo': photo})

        return redirect('profile_detail', self.kwargs['pk'])
