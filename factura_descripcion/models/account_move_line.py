# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Campos de odoo studio para recrear sus funciones

    x_studio_rentabilidad = fields.Monetary(
        string="Rentabilidad",
        compute="_compute_rentability",
        readonly=True,
    )

    x_studio_pu_con_descuento = fields.Monetary(
        string="PU con Descuento",
        compute="_compute_pu_con_descuento",
        readonly=True,
    )

    x_studio_costo = fields.Float(
        string="Costo",
        related="product_id.standard_price",
        readonly=True,
        store=True,
    )

    # Metodos computados

    @api.depends('price_unit')
    def _compute_rentability(self):
        for record in self:
            if record.move_id.type == "out_refund":
                rentability = record.x_studio_pu_con_descuento - record.x_studio_costo
                if rentability < 0:
                    rentability = record.x_studio_pu_con_descuento
                record[("x_studio_rentabilidad")] = rentability
            else:
                if record.move_id.currency_id.name == 'USD':
                    cop = self.env['res.currency.rate'].search([('currency_id.id', '=', 8), ('name', '=', record.move_id.date_invoice)])
                    if cop:
                        record[("x_studio_rentabilidad")] = (record.x_studio_pu_con_descuento * cop.rate) - record.x_studio_costo
                    else:
                        record[(
                            "x_studio_rentabilidad")] = record.x_studio_pu_con_descuento - record.x_studio_costo
                else:
                    record[(
                        "x_studio_rentabilidad")] = record.x_studio_pu_con_descuento - record.x_studio_costo

    @api.depends('price_unit')
    def _compute_pu_con_descuento(self):
        for record in self:
            if record.discount > 0:
                record.x_studio_pu_con_descuento = record.price_unit - ((record.price_unit * record.discount) / 100)
            else:
                record.x_studio_pu_con_descuento = record.price_unit