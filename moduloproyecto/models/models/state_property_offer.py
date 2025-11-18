# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError

class StatePropertyOffer(models.Model):
    _name = "state.property.offer" #el punto lo interpreta como _ (esto solo ocurre en el nombre y crea una tabla en BBDD con este campo con _)
    _description = "Property Offer"
    
    price = fields.Float('Price')
    status = fields.Selection([
        ('Accepted', 'Accepted'),['Refused','Refused']
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    state_property_id = fields.Many2one('state.property', string='Property', required=True)
    
    def cancelaroferta(self):
        for record in self:
            record.status = "Refused"
            
    def aprobaroferta(self):
        for record in self:
            registro = record.state_property_id.state_property_offer_ids.filtered(lambda line: line.status == "Accepted")
            if len(registro) > 0:
                 raise UserError(_("Ya existe una oferta y no se puede aceptar"))
            else:
                record.status = "Accepted"
        