import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    time = timezone.localtime()
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=time,
        disappeared_at__gte=time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon_entities:
            if pokemon_entity.pokemon.image:
                image_url = request.build_absolute_uri(
                    pokemon_entity.pokemon.image.url
                )
                add_pokemon(
                    folium_map, pokemon_entity.lat,
                    pokemon_entity.lon,
                    image_url
                )

    pokemons_on_page = []
    for pokemon in pokemons:
        image_url = None
        if pokemon.image:
            image_url = request.build_absolute_uri(
                    pokemon.image.url
                )
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    time = timezone.localtime()
    pokemon = Pokemon.objects.get(id=pokemon_id)
    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_render = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(
            pokemon.image.url
        ),
    }

    if pokemon.previous_evolution:
        pokemon_render['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(
                pokemon.previous_evolution.image.url
            )
        }
    if pokemon.pokemon_set.all():
        next_evolution = pokemon.pokemon_set.all()[0]
        pokemon_render['next_evolution'] = {
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(
                next_evolution.image.url
            )
        }

    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=time,
        disappeared_at__gte=time,
        pokemon=pokemon
    )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                pokemon.image.url
            )
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_render
    })
