# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Campo que relaciona una factura con todos sus pagos
    payments = fields.Many2many(
        comodel_name="account.payment",
        compute='_compute_payment_ids'
    )

    # rentabilidad generada en la factura
    x_studio_rentabilidad = fields.Monetary(
        string="Rentabilidad",
        readonly=True,
        compute="_compute_rentabilidad",
        store=True,
        default=0.0
    )

    x_studio_costo_total = fields.Monetary(
        string="Costo Total",
        readonly=True,
        compute="_compute_costo_total",
        default=0.0
    )

    x_studio_rentabilidad_por = fields.Float(
        string="Rentabilidad %",
        readonly=True,
        compute="_compute_studio_rentabilidad_por",
        default=0.0
    )

    x_studio_base_imponible_cop = fields.Monetary(
        string="Base imponible (COP)",
        readonly=True,
        compute="_compute_base_imponible_cop",
        store=True,
        default=0.0
    )

    x_studio_trm = fields.Monetary(
        string="TRM",
        readonly=True,
        compute="_compute_trm",
        default=0.0
    )

    def _compute_payment_ids(self):
        for record in self:
            record.payments = self.env['account.payment'].search([('invoice_ids', 'in', record.id)]).sorted(key=lambda r: r.id)

    @api.depends('x_studio_costo_total')
    def _compute_rentabilidad(self):
        for record in self:
            total_rentabilidad = 0
            for linea in record.invoice_line_ids:
                total_rentabilidad += linea.x_studio_rentabilidad * linea.quantity
            record.x_studio_rentabilidad = total_rentabilidad

    @api.depends('amount_untaxed')
    def _compute_costo_total(self):
        for record in self:
            total_costo = 0
            for linea in record.invoice_line_ids:
                total_costo = total_costo + (
                            linea.x_studio_costo * linea.quantity)
            record.x_studio_costo_total = total_costo

    @api.depends('x_studio_rentabilidad')
    def _compute_studio_rentabilidad_por(self):
        for record in self:
            if record.amount_untaxed > 0:
                if record.currency_id.name == 'USD':
                    if record.x_studio_base_imponible_cop > 0:
                        record.x_studio_rentabilidad_por = (record.x_studio_rentabilidad * 100) / record.x_studio_base_imponible_cop
                    else:
                        record.x_studio_rentabilidad_por = 0
                else:
                    record.x_studio_rentabilidad_por = (record.x_studio_rentabilidad * 100) / record.amount_untaxed
            else:
                record.x_studio_rentabilidad_por = 0

    @api.depends('amount_untaxed')
    def _compute_base_imponible_cop(self):
        for record in self:
            if record.currency_id.name == 'USD':
                record.x_studio_base_imponible_cop = (record.amount_untaxed * record.x_studio_trm)
            else:
                record.x_studio_base_imponible_cop = record.amount_untaxed

    @api.depends('currency_id', 'invoice_date')
    def _compute_trm(self):
        for record in self:
            if record.currency_id.name == 'USD':
                cop = self.env['res.currency.rate'].search([('currency_id.id', '=', 8), ('name', '=', record.invoice_date)])
                if cop:
                    record.x_studio_trm = cop.rate
                else:
                    record.x_studio_trm = 0
            else:
                record.x_studio_trm = 0