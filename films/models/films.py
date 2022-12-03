# -*- coding: utf-8 -*-
import base64

import requests

from odoo import api, fields, models


class Film(models.Model):
    _name = 'films.film'
    _description = 'Film'
    _order = 'create_date'

    search_field = fields.Char()
    name = fields.Char(string="Film name", required=True, unique=True, help="Название фильма")
    big_poster = fields.Image("Film poster big")
    small_poster = fields.Image("Film poster small")
    errors_message = fields.Char('Ошибка')
    errors = fields.Boolean(default=False)


    def _get_film_data(self):
        url = f'https://kinobd.ru/api/films/search/title?q={self.search_field}'
        headers = {'User-Agent': 'odoo-app'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()['data']
        if response.status_code == 200 and response_data:
            data = {
                'name': response_data[0]['name_russian'],
                'big_poster': response_data[0]['big_poster'],
                'small_poster': response_data[0]['small_poster'],
            }
        else:
            data = {
                'errors': True
            }
        return data


    def load_image_from_url(self, url):
        data = base64.b64encode(requests.get(url.strip()).content).replace(b'\n', b'')
        return data

    @api.onchange('search_field')
    def onchange_search_field(self):
        if self.search_field:
            result = self._get_film_data()
            if 'errors' in result:
                self.errors = True
                self.errors_message = 'Ошибка запроса'
            else:
                self.errors = False
                self.name = result.get('name')
                self.big_poster = self.load_image_from_url(result.get('big_poster'))
                self.small_poster = self.load_image_from_url(result.get('small_poster'))
                self.search_field = None

