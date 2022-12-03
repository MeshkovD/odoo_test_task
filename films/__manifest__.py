# -*- coding: utf-8 -*-

{
    'name': 'Films',
    'author': 'D.I.',
    'version': '1.0.0',
    'category': 'Films/films',
    'sequence': 0,
    'summary': 'Films information',
    'description': """Внимание! Данный модуль кастомизирует стандартную модель Компании, превращая все компании в кинотеатры""",
    'depends': ['contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/film_menu.xml',
        'views/film_views.xml',
        'views/ticket_views.xml',
        'views/res_partner_inherit.xml',
    ],
    'application': True,
}
