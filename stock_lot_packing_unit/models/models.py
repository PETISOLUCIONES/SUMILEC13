# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    qty_packing = fields.Float(string='Cantidad de empaque', default=0)

    _sql_constraints = [('qty_packing', 'CHECK(qty_packing >= 0)', 'La cantidad de empaque debe ser mayor o igual a 0')]


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_done(self):
        res = super(StockPicking, self).action_done()
        if res:
            for move in self:
                if move.picking_type_id.code == 'outgoing':
                    for line in move.move_line_ids:
                        qty_done = line.qty_done
                        if line.lot_id and line.lot_id.qty_packing != 0:
                            quants = move.env['stock.quant']._gather(line.product_id, line.location_id, lot_id=line.lot_id, strict=True)
                            if quants.quantity % line.lot_id.qty_packing != 0:
                                qty_restante = quants.quantity % line.lot_id.qty_packing
                                new_qty = - qty_restante
                                quants._update_available_quantity(
                                    line.product_id, line.location_id, new_qty, lot_id=line.lot_id)
                                #quants.sudo().write({'quantity': new_qty})
                                quant_free = move.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('quantity', '=', 0)], limit=1)
                                qty_movida = False
                                for quant in quant_free:
                                    if quant.quantity == 0:
                                        qty_movida = True
                                        quant._update_available_quantity(
                                            quant.product_id, quant.location_id, qty_restante, lot_id=quant.lot_id)
                                        quant.lot_id.write({'qty_packing': 0})
                                if not qty_movida:
                                    vals_lot = {
                                        'product_id': line.product_id.id,
                                        'company_id': self.env.company.id,
                                    }
                                    lot = move.env['stock.production.lot'].create(vals_lot)
                                    '''vals = {
                                        'product_id': line.product_id.id,
                                        'location_id': line.location_id.id,
                                        'quantity': qty_restante,
                                        'lot_id': lot.id
                                    }'''
                                    move.env['stock.quant']._update_available_quantity(
                                        line.product_id, line.location_id, qty_restante, lot_id=lot)

                                    #move.env['stock.quant'].sudo().create(vals)
        return res











