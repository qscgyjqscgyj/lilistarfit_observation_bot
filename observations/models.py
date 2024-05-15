from django.db import models
from django.core import serializers

class ReferenceNorms(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    value_man = models.CharField(max_length=255, verbose_name='Норма для мужчин')
    value_woman = models.CharField(max_length=255, verbose_name='Норма для женщин')
    description = models.TextField(verbose_name='Описание')
    reasons = models.TextField(verbose_name='Причины отклонения')
    conclusion = models.TextField(verbose_name='Заключение')
    ai_generated = models.BooleanField(default=False, verbose_name='Сгенерировано ИИ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    @staticmethod
    def get_norms_payload(cls):
        norms = cls.objects.all()
        payload =  serializers.serialize('json', norms)
        return payload

    @staticmethod
    def import_norms(cls, import_norms):
        existing_norms_names = cls.objects.values_list('name', flat=True)

        norms_objects = []
        for import_norm_data in import_norms:
            if import_norm_data['name'] in existing_norms_names:
                continue

            new_norm = cls(**import_norm_data)
            norms_objects.append(new_norm)

        cls.objects.bulk_create(norms_objects)
        return True

    class Meta:
        verbose_name = 'Нормы'
        verbose_name_plural = 'Нормы'
        ordering = ['name']


class Chat(models.Model):
    chat_id = models.CharField(max_length=255, unique=True, verbose_name='ID чата')
    last_messages = models.JSONField(verbose_name='Последние сообщения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.chat_id

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['chat_id']
