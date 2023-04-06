import re
import string

import django.core.exceptions
from django.db import models


class NameWithDetailAbstractModel(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='название',
        help_text='как называется?',
    )
    detail = models.TextField(
        verbose_name='детали',
        help_text='более подробное описание',
        null=True,
    )

    class Meta:
        abstract = True


class UniqueNameWithDetailAbstractModel(NameWithDetailAbstractModel):
    is_cleaned = False
    similar_english_to_russian_letters = {
        'a': 'а',
        'e': 'е',
        'p': 'р',
        'o': 'о',
        'x': 'х',
        'y': 'у',
        'c': 'с',
        't': 'т',
        'h': 'н',
        'b': 'в',
        'k': 'к',
        'm': 'м',
    }
    msg = 'Кажется, похожее название уже существует!'
    unique_name = models.CharField(
        verbose_name='уникальное имя',
        help_text='Колонка для проверки уникальности названия',
        max_length=150,
        unique=True,
        null=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def generate_normalized_name(self):
        normalized_name_english = ''
        normalized_name_russian = ''
        for letter in list(
            ''.join(re.split(f'[{string.punctuation} ]', self.name.lower()))
        ):
            if letter:
                for (
                    eng_letter,
                    rus_letter,
                ) in self.similar_english_to_russian_letters.items():
                    if letter == eng_letter:
                        normalized_name_english += letter
                        normalized_name_russian += rus_letter
                        break
                    if letter == rus_letter:
                        normalized_name_russian += letter
                        normalized_name_english += eng_letter
                        break
                else:
                    normalized_name_russian += letter
                    normalized_name_english += letter
        name_checking_1 = self.__class__.objects.filter(
            unique_name=normalized_name_english
        )
        name_checking_2 = self.__class__.objects.filter(
            unique_name=normalized_name_russian
        )
        if not name_checking_1 and not name_checking_2:
            self.unique_name = normalized_name_russian
            return super().clean()
        raise django.core.exceptions.ValidationError(self.msg)

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        self.is_cleaned = True
        self.generate_normalized_name()
