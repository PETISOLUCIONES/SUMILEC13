# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AccountInvoiceRefund(models.TransientModel):
    _inherit = 'account.move.reversal'

    reason_id = fields.Many2one('account.invoice.refund.reason',
                                string="Reason to credit")

    @api.onchange('reason_id')
    def _onchange_reason_id(self):
        if self.reason_id:
            self.reason = self.reason_id.name

    def _prepare_default_reversal(self, move):
        res = super()._prepare_default_reversal(move)
        res['reason_id'] = self.reason_id.id
        return res
