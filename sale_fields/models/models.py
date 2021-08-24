# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    nit_partner = fields.Char(string='NIT', related='partner_id.vat')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmation_date = fields.Datetime(string='Confirmation Date', readonly=True, index=True, help="Date on which the sales order is confirmed.", copy=False)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.write({
            'confirmation_date': fields.Datetime.now()
        })
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    category_id = fields.Many2one('product.category', related='product_id.categ_id', string='Marca o Categoria')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_seller_code = fields.Char(string="Referencia Proveedor", compute="_get_product_seller_code", readonly=True)

    def _get_product_seller_code(self):
        if self.seller_ids and self.seller_ids[0].product_code:
            self.product_seller_code = self.seller_ids[0].product_code
        else:
            self.product_seller_code = ""

