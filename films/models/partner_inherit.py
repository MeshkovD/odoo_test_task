from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_cinema = fields.Boolean('Является кинотеатром')
    ticket_ids = fields.One2many('films.ticket', 'partner_id')
