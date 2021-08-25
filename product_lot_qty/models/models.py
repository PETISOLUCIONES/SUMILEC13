# -*- coding: utf-8 -*-

from odoo import models, fields, api

class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    reservado = fields.Float(compute='_determinar_reservado')

    def _determinar_reservado(self):
        for record in self:
            reser = 0
            for quant in record.quant_ids:
                reser += quant.reserved_quantity
            record.reservado = reser