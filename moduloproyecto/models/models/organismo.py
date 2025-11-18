# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

TICKET_PRIORITY = [
    ('0', 'Low priority'),
    ('1', 'Medium priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]

class Organismo(models.Model):
    _name = "organismo"
    _description = "organismo nuevo modelo"
    
    name = fields.Char(required=True,default="Nuevo organismo",string="Title")
    description = fields.Text()
    numregistro = fields.Char(required=True,string="Numero_Registro")
    priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='0')
    active = fields.Boolean(string="Activo", default=True)
    start_date= fields.Date(default=fields.Date.today())