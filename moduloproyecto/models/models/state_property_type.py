# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "state.property.type" #el punto lo interpreta como _ (esto solo ocurre en el nombre y crea una tabla en BBDD con este campo con _)
    _description = "Curso Nuevo Módulo Tipo"
    
    name = fields.Char(required=True,default="Nuevo registro",string="Title")
    state_property_ids = fields.One2many("state.property", "state_property_type_id", string="Properties") #IDS SIEMPRE AL FINAL POR CONVENCION: MODELO, NOMBRE DEL CAMPO MANY2ONE, STRING QUE ES EL LITERAL DEL CAMPO