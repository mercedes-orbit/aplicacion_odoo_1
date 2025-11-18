# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

class StateProperty(models.Model):
    _name = "state.property" #el punto lo interpreta como _ (esto solo ocurre en el nombre y crea una tabla en BBDD con este campo con _)
    _inherit = ['mail.thread', 'mail.activity.mixin'] #HEREDA DE MAIL.THREAD Y MAIL.ACTIVCITY.MIXIN
    _description = "Curso Nuevo Módulo"
    _order = "sequence, name, id"
    
    name = fields.Char(required=True,default="Nuevo registro",string="Title") #coloca en tabla bbdd not null, por defecto es null
    description = fields.Text()
    address = fields.Text()
    province = fields.Char()
    country = fields.Char()
    postcode = fields.Char(default="28022")
    date_availability= fields.Date(default=fields.Date.today())
    expected_price= fields.Float(required=True,default=10.23)
    selling_price= fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden= fields.Boolean()
    garden_area= fields.Integer()
    garden_orientation = fields.Selection([("North", "NorthTexto"),
                                          ("South", "SouthTexto"),
                                          ("East", "EastTexto"),
                                          ("West", "WestTexto")], default="West")
    active = fields.Boolean(default=True)  #reservado de ODOO
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    state = fields.Selection([("New", "New"),
                                          ("Offer", "Offer"),
                                          ("Accepted", "Accepted"),
                                          ("Sold", "Sold"),
                                          ("Canceled", "Canceled")], default="New")  #reservado de ODOO
    available_from = fields.Date()
    
    seller_id = fields.Many2one("res.partner", string="Seller") #SIEMPRE EL ID AL FINAL POR CONVENCION EN LOS CAMPOS MANY2ONE
    state_property_type_id = fields.Many2one(string='Type', comodel_name="state.property.type") #SI NO SE PONE EL MODELO COMO PRIMER PARAMETRO, SE TIENE QUE LLAMAR COMODEL_NAME
    buyer_id = fields.Many2one("res.partner", string="Buyer") #MODULO contactos y el MODELO es res.partner (se ve en la url cuando se abre la aplicación y su vista)
    sale_order_ids = fields.Many2many("sale.order") #SIEMPRE IDS AL FINAL POR CONVENCION EN LOS CAMPOS MANY2MANY
    state_property_offer_ids = fields.One2many("state.property.offer", "state_property_id", string="Offers")
    best_offer = fields.Float(compute="_compute_best_offer")
    total = fields.Float(compute="_compute_total", inverse="_inverse_total")
    text = fields.Char(compute="_compute_text", inverse="_inverse_text", store=True)
    
    state_property_tag_ids = fields.Many2many("state.property.tag") #poner el nombre del modelo con puntos
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    
    #EVENTOS Y CAMPOS CALCULADOS    
    
    #EVENTOS DELETE Y DUPLICATE SON DOS EVENTOS EN LA RUEDITA ACCIONES DE UN FORMULARIO
    @api.ondelete(at_uninstall=False)
    def _ondelete_property(self):
        if (self.state == "Canceled" or self.state == "New"):
            raise UserError(_("No puede eliminarse una propiedad que ya está cancelada o se esta creando"))
        #NO HACE FALTA UN ELSE, SE BORRARIA EL REGISTRO DEL RESTO DE ESTADOS
        
    @api.onchange('seller_id')
    def _onchange_seller_id(self):
        if self.seller_id:
            self.province = "%s" % self.seller_id.city
        else:
            self.province = ""
            
    #@api.onchange('selling_price')
    #def _onchange_selling_price(self):
        #if float_is_zero(self.selling_price, 2) == True:
            #raise ValidationError(_("El precio de venta no pueda ser 0"))
        #else:
            #if float_compare(self.selling_price, self.expected_price, 2) == 0:
                #raise ValidationError(_("El precio de venta no pueda ser igual al precio esperado"))
            #elif float_compare(self.selling_price, self.expected_price, 2) == 1:   
                #raise ValidationError(_("El precio de venta no pueda ser superior al precio esperado")) 
            #else: 
                #if float_is_zero(self.expected_price, 2) == False:
                    #tantoporciento = (self.expected_price * 90) / 100
                    #if self.selling_price < tantoporciento:
                        #raise ValidationError(_("El precio de venta no pueda ser inferior al 90% del precio esperado")) 
    #float_compare                
    #-1 : If the first value is less than the second value.
    # 0 : If the first value is equal to the second value.
    # 1 : If the first value is greater than the second value.	
    
    #@api.onchange('expected_price')
    #def _onchange_expected_price(self):
        #if float_is_zero(self.expected_price, 2) == True:
            #raise ValidationError(_("El precio esperado no pueda ser 0"))
        #else:
            #if float_compare(self.selling_price, self.expected_price, 2) == 0:
                #raise ValidationError(_("El precio de venta no pueda ser igual al precio esperado"))
            #elif float_compare(self.selling_price, self.expected_price, 2) == 1:   
                #raise ValidationError(_("El precio de venta no pueda ser superior al precio esperado")) 
            #else:
                #if float_is_zero(self.expected_price, 2) == False:     
                    #tantoporciento = (self.expected_price * 90) / 100
                    #if self.selling_price < tantoporciento:
                        #raise ValidationError(_("El precio de venta no pueda ser inferior al 90% del precio esperado")) 
                            
    @api.depends("state_property_offer_ids")
    def _compute_best_offer(self):
        for record in self:
            best_offer_price = 0.0
            if len(record.state_property_offer_ids) > 0:
                best_offer_price = min(record.state_property_offer_ids.mapped("price"))
            record.best_offer = best_offer_price
            
    @api.depends("state_property_offer_ids")
    def _compute_total(self):
        for record in self:
            #record.total = (record.best_offer * 2)
            record.total = record.state_property_offer_ids.filtered(lambda line: line.status == "Accepted").price
                
    def _inverse_total(self):
        for record in self:
            record.total = (record.best_offer / 2)
    
    def _inverse_text(self):
        pass
                    
    @api.depends("name")
    def _compute_text(self):
        for record in self:
            record.text = "test for name %s" % record.name
            
    def cancelarproperty(self):
        for record in self:
            if (record.state != "Canceled"):
                record.state = "Canceled"
            else:
                raise UserError(_("No puede cancelarse una propiedad que ya está cancelada"))
            
    def venderproperty(self):
        for record in self:
            if (record.state == "Sold"):
                raise UserError(_("No puede venderse una propiedad que ya está vendida"))    
            elif (record.state == "Canceled"):
                raise UserError(_("No puede venderse una propiedad que ya está cancelada"))
            else:
                record.state = "Sold"