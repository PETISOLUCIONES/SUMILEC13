
from odoo import models, fields, api




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    purchase_price = fields.Float(string='Cost', digits='Product Price', groups="permisos_super.user_master")
    purchase_price_com = fields.Float(string='Cost', compute='onchange_cost')

    @api.onchange('purchase_price')
    def onchange_cost(self):
        self.purchase_price_com = self.purchase_price







