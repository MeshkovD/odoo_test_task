# -*- coding: utf-8 -*-
import base64

import requests

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command


class Ticket(models.Model):
    _name = 'films.ticket'
    _description = 'Ticket'
    _order = 'create_date'

    partner_id = fields.Many2one('res.partner', string='Покупатель')
    company_id = fields.Many2one('res.partner', string='Кинотеатр')
    film_id = fields.Many2one('films.film', string='Фильм')
    film_date = fields.Datetime('Время')

