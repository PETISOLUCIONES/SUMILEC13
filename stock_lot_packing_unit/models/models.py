# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare, float_round, float_is_zero

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
                    rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
                    for line in move.move_line_ids:
                        qty_done = line.qty_done
                        if line.lot_id and line.lot_id.qty_packing != 0 and line.product_id.tracking != 'none':
                            quants = move.env['stock.quant']._gather(line.product_id, line.location_id, lot_id=line.lot_id, strict=True)
                            if quants.quantity % line.lot_id.qty_packing != 0:
                                qty_restante = quants.quantity % line.lot_id.qty_packing
                                new_qty = - qty_restante
                                quants._update_available_quantity(
                                    line.product_id, line.location_id, new_qty, lot_id=line.lot_id)
                                #quants.sudo().write({'quantity': new_qty})
                                lot_free = move.env['stock.production.lot'].search([('product_id', '=', line.product_id.id)])
                                #quant_free = move.env['stock.quant'].search([('product_id', '=', line.product_id.id)], limit=1)
                                qty_movida = False
                                for lot in lot_free:
                                    if float_compare(lot.product_qty, 0, precision_digits=rounding) == 0:
                                        qty_movida = True
                                        self.env['stock.quant']._update_available_quantity(
                                            line.product_id, line.location_id, qty_restante, lot_id=lot)
                                        break
                                if not qty_movida:
                                    name = self.create_name_lot(line.product_id.id)
                                    vals_lot = {
                                        'name': name,
                                        'product_id': line.product_id.id,
                                        'company_id': self.env.company.id,
                                    }
                                    lot = move.env['stock.production.lot'].create(vals_lot)

                                    move.env['stock.quant']._update_available_quantity(
                                        line.product_id, line.location_id, qty_restante, lot_id=lot)
                                '''for quant in quant_free:
                                    if float_compare(quant.quantity, 0, precision_digits=rounding) == 0:
                                        qty_movida = True
                                        quant._update_available_quantity(
                                            quant.product_id, quant.location_id, qty_restante, lot_id=lot_free.id)
                                        quant.lot_id.write({'qty_packing': 0})'''
                                '''if not qty_movida:
                                    name = self.create_name_lot(line.product_id.id)
                                    vals_lot = {
                                        'name': name,
                                        'product_id': line.product_id.id,
                                        'company_id': self.env.company.id,
                                    }
                                    lot = move.env['stock.production.lot'].create(vals_lot)

                                    move.env['stock.quant']._update_available_quantity(
                                        line.product_id, line.location_id, qty_restante, lot_id=lot)'''

                                    #move.env['stock.quant'].sudo().create(vals)
        return res

    def create_name_lot(self, product_id):
        lot_count = self.env['stock.production.lot'].search_count([('product_id', '=', product_id)])
        if lot_count != 0:
            if len(str(lot_count)) >= 3:
                name = str(lot_count+1)
            elif len(str(lot_count)) == 2:
                name = "0" + str(lot_count+1)
            elif len(str(lot_count)) == 1:
                name = "00" + str(lot_count+1)
        else:
            name = "001"
        name_count = self.env['stock.production.lot'].search_count([('name', '=', name), ('product_id', '=', product_id)])
        if name_count > 0:
            return False
        return name












