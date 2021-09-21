# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Campo para el calculo de rentabilidad
    x_studio_rentabilidad = fields.Monetary(
        string="Rentabilidad",
        compute="_compute_rentability",
        readonly=True,
        store=True,
    )

    x_studio_porcentaje_rentabilidad = fields.Float(
        string="% Rentabilidad",
        compute="_compute_rentaility_percentage",
        readonly=True,
        store=True,
    )

    x_minimo_rentabilidad = fields.Float(string='% Minimo Rentabilidad',  related="categ_id.x_studio_por_minimo_rentabilidad", readonly=True)



    @api.depends('list_price')
    def _compute_rentability(self):
        for record in self:
            record.x_studio_rentabilidad = record.list_price - record.standard_price

    @api.depends('x_studio_rentabilidad')
    def _compute_rentaility_percentage(self):
        for record in self:
            if float_compare(record.list_price, 0.0, precision_rounding=record.uom_id.rounding) != 0:
                record.x_studio_porcentaje_rentabilidad = (record.x_studio_rentabilidad * 100) / record.list_price
