# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StatePropertyTag(models.Model):
    _name = "state.property.tag" #el punto lo interpreta como _ (esto solo ocurre en el nombre y crea una tabla en BBDD con este campo con _)
    _description = "Property Tag"
    
    name = fields.Char('Title')
    color = fields.Integer("Color")
    
    _sql_constraints = [("name_unique", "unique(name)", "No pueden repetirse los nombres de las etiquetas")]