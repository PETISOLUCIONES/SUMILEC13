from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    category_id = fields.Many2one('product.category', related='product_id.categ_id', string='Marca o Categoria')


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    category_id = fields.Many2one('product.category', related='product_id.categ_id', string='Marca o Categoria')
