# Copyright 2017 Camptocamp SA - Damien Crier, Alexandre Fayolle
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sequence = fields.Integer(help="Shows the sequence of this line in the "
                              " invoice.", default=9999,
                              string="Item")

    # shows sequence on the invoice line
    sequence2 = fields.Integer(help="Shows the sequence of this line in the "
                               " invoice.", related='sequence',
                               string="Item", store=True)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line')
    def _compute_max_line_sequence(self):
        """Allow to know the highest sequence entered in invoice lines.
        Then we add 1 to this value for the next sequence.
        This value is given to the context of the o2m field in the view.
        So when we create new invoice lines, the sequence is automatically
        added as :  max_sequence + 1
        """
        for order in self:
            order.max_line_sequence = (
                max(order.mapped('order_line.sequence') or [0]) + 1)

    max_line_sequence = fields.Integer(string='Max sequence in lines',
                                       compute='_compute_max_line_sequence',
                                       store=True)

    def _reset_sequence(self):
        for rec in self:
            for current_seq, line in enumerate(rec.order_line, start=1):
                line.sequence = current_seq

    def write(self, values):
        res = super(PurchaseOrder, self).write(values)
        self._reset_sequence()
        return res
