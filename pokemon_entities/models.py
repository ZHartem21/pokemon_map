from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    image = models.ImageField(null=True, blank=True, verbose_name='картинка')
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='английское название'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='японское название'
    )
    description = models.TextField(blank=True, verbose_name='описание')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='предыдущая эволюция',
        related_name='next_evolutions'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='покемон',
        related_name='entities'
    )
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(null=True, verbose_name='появится')
    disappeared_at = models.DateTimeField(null=True, verbose_name='исчезнет')
    level = models.IntegerField(null=True, blank=True, verbose_name='долгота')
    health = models.IntegerField(null=True, blank=True, verbose_name='здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='броня')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='выносливость')
