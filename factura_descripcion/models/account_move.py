# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_is_zero
import json



class AccountMove(models.Model):
    _inherit = 'account.move'

    # Campo que relaciona una factura con todos sus pagos
    payments = fields.Many2many(
        comodel_name="account.payment",
        compute='_compute_payment_ids'
    )

    # Campo pagado en diario, hace referencia al diario del primer pago registrado
    payment_in_journal = fields.Many2one(
        string="Pagado en diario",
        comodel_name="account.journal",
        compute="_compute_payment_in_journal",
        store=True
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

    @api.depends('payments', 'state', 'invoice_payment_state')
    def _compute_payment_in_journal(self):
        for record in self:
            payments = self.env['account.payment'].search(
                [('invoice_ids', 'in', record.id)]).sorted(key=lambda r: r.id)
            if payments:
                record.payment_in_journal = payments[0].journal_id
            else:
                record.payment_in_journal = None

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

    def _compute_payments_widget_to_reconcile_info(self):
        for move in self:
            move.invoice_outstanding_credits_debits_widget = json.dumps(False)
            move.invoice_has_outstanding = False

            if move.state != 'posted' or move.invoice_payment_state != 'not_paid' or not move.is_invoice(include_receipts=True):
                continue
            pay_term_line_ids = move.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))

            domain = [('account_id', 'in', pay_term_line_ids.mapped('account_id').ids),
                      '|', ('move_id.state', '=', 'posted'), '&', ('move_id.state', '=', 'draft'), ('journal_id.post_at', '=', 'bank_rec'),
                      ('partner_id', '=', move.commercial_partner_id.id),
                      ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0),
                      ('amount_residual_currency', '!=', 0.0)]

            if move.is_inbound():
                domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                type_payment = _('Outstanding credits')
            else:
                domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                type_payment = _('Outstanding debits')
            info = {'title': '', 'outstanding': True, 'content': [], 'move_id': move.id}
            lines = self.env['account.move.line'].search(domain)
            currency_id = move.currency_id
            if len(lines) != 0:
                for line in lines:
                    # get the outstanding residual value in invoice currency
                    if line.currency_id and line.currency_id == move.currency_id:
                        amount_to_show = abs(line.amount_residual_currency)
                    else:
                        currency = line.company_id.currency_id
                        amount_to_show = currency._convert(abs(line.amount_residual), move.currency_id, move.company_id,
                                                           line.date or fields.Date.today())
                    if float_is_zero(amount_to_show, precision_rounding=move.currency_id.rounding):
                        continue
                    info['content'].append({
                        'journal_name': line.move_id.name or line.ref,
                        'amount': amount_to_show,
                        'currency': currency_id.symbol,
                        'id': line.id,
                        'position': currency_id.position,
                        'digits': [69, move.currency_id.decimal_places],
                        'payment_date': fields.Date.to_string(line.date),
                    })
                info['title'] = type_payment
                move.invoice_outstanding_credits_debits_widget = json.dumps(info)
                move.invoice_has_outstanding = True