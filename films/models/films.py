# -*- coding: utf-8 -*-
import base64

import requests

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TempFilm(models.Model):
    _name = 'films.temp_film'

    name = fields.Char(string="Film name", required=True, unique=True, help="Название фильма")
    small_poster = fields.Image("Film poster small")
    film_id = fields.One2many('films.film', 'temp_film_id', string='Фильм')



class Film(models.Model):
    _name = 'films.film'
    _description = 'Film'
    _order = 'create_date'

    search_field = fields.Char()
    name = fields.Char(string="Film name", unique=True, help="Название фильма")
    small_poster = fields.Image("Film poster small")
    temp_film_id = fields.Many2one('films.temp_film')

    def _get_film_data(self):
        url = f'https://kinobd.ru/api/films/search/title?q={self.search_field}'
        headers = {'User-Agent': 'odoo-app'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()['data']
        if not response_data:
            raise ValidationError(f'Информация по запросу {self.search_field} не найдена')
        elif response.status_code != 200:
            raise ValidationError(f'Ошибка запроса({response.status_code})')
        return response_data

    def load_image_from_url(self, url):
        data = None
        if url:
            data = base64.b64encode(requests.get(url.strip()).content).replace(b'\n', b'')
        return data

    @api.onchange('temp_film_id')
    def onchange_temp_film_id(self):
        if self.search_field:
            self.name = self.temp_film_id.name
            self.small_poster = self.temp_film_id.small_poster


    def search_button(self):
        if self.search_field:

            temp_films = self.env['films.temp_film'].search([])
            temp_films.unlink()

            films_data = self._get_film_data()
            _list = []

            for film in films_data:
                self.env['films.temp_film'].create({
                    'name': film.get('name_russian', 'Имя не указано'),
                    'small_poster': self.load_image_from_url(film.get('small_poster', None)),
                    'film_id': [self.id]})

