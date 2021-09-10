# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Se hereda la función que calcula las cantidades
    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity')
    def _get_invoice_qty(self):
        for line in self:
            qty_invoiced = 0.0
            for invoice_line in line.invoice_lines:
                if invoice_line.move_id.state != 'cancel':
                    if invoice_line.move_id.type == 'out_invoice':
                        qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
                    elif invoice_line.move_id.type == 'out_refund':
                        # Se busca la linea de la cual procede la devolución,
                        # Si el precio es igual se descuentan las unidades
                        # Si es diferente entonces no se descuenta
                        invoice = invoice_line.move_id.reversed_entry_id
                        if invoice.line_ids:
                            for rev_line in invoice.line_ids:
                                if rev_line.product_id == invoice_line.product_id and rev_line.price_unit == invoice_line.price_unit:
                                    qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
            line.qty_invoiced = qty_invoiced
