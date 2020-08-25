from django.core.exceptions import PermissionDenied


class AccessToEditAndDeleteDataMixin():
    """Класс проверяет доступ к редактированию и удалению данных"""

    def userVerification(self):
        """Проверяет пользователя, является ли пользователь владельцем данных либо администратором сайта"""
        return self.get_object().user == self.request.user or self.request.user.is_staff

    def dispath(self, request, *args, **kwargs):
        """Посредник между запросом и ответом. Переопределяет метод dispath"""
        if not self.userVerification():
            raise PermissionDenied  # Ошибка 403, Отказано в доступе

        return super().dispath(request, *args, **kwargs)
