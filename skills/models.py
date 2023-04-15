from core.models import ShortUniqueNameAbstractModel


class Skill(ShortUniqueNameAbstractModel):
    class Meta:
        verbose_name = 'навык'
        verbose_name_plural = 'навыки'
        default_related_name = 'skills'

    def __str__(self):
        return self.name
