from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


def get_path_image(user_name, image_name):
    """Метод получения адреса сохранения изображений"""
    return str(user_name) + '/' + str(image_name)


class Gallery(models.Model):
    """Модель галереии, связь с моделю объявлений и изображений"""
    title = models.CharField('Название галереии', max_length=41)
    slug = models.SlugField('URL', max_length=41, null=True)
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('gallery_update', kwargs={'slug': self.slug})

    def get_delete_form_url(self):
        return reverse('galery_delete', kwargs={'slug': self.slug})

    class Meta:
        """Представление модели в административной панели"""
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'
        ordering = ['-pk']


class Image(models.Model):
    """Модель изображений, входящий в модель галереии"""
    title = models.CharField('Описание', max_length=35, blank=True)
    image = models.ImageField('Изображение', upload_to='advert/')
    gallery = models.ForeignKey(
        Gallery, verbose_name='Галерея', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Переопределение метода save, для переопределения адреса сохранения изображений"""
        self.image.name = get_path_image(self.user, self.image.name)
        super().save(**kwargs)
    
    def get_delete_form_url(self):
        return reverse('image_delete', kwargs={'pk': self.pk, 'gallery': self.gallery.slug})

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'Изображение в галереии: ' + str(self.gallery) + '(№' + str(self.pk) + ')'

    class Meta:
        """Представление модели в административной панели"""
        verbose_name = 'Изображение объявления'
        verbose_name_plural = 'Изображения объявлений'
