# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.stock.models.product import OPERATORS
from odoo.tools.float_utils import float_round


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    nit_partner = fields.Char(string='NIT', related='partner_id.vat')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmation_date = fields.Datetime(string='Confirmation Date', readonly=True, index=True, help="Date on which the sales order is confirmed.", copy=False)
    x_studio_permitir_menor_al_costo = fields.Boolean()

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.write({
            'confirmation_date': fields.Datetime.now()
        })
        return res

    #@api.model
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for record in self:
            for linea in record.order_line:
                if linea.price_reduce < linea.purchase_price:
                    if not record.x_studio_permitir_menor_al_costo:
                        if record.state != 'sale':
                            raise UserError('NO puede vender a un precio menor al costo ')
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    category_id = fields.Many2one('product.category', related='product_id.categ_id', string='Marca o Categoria')
    cantidad_disponible = fields.Float(related='product_id.qty_available_not_res', string='cantidad disponible')
    minimo_rentabilidad = fields.Float(related='category_id.x_studio_por_minimo_rentabilidad', string='% Mínimo Rentabilidad')





class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_seller_code = fields.Char(string="Referencia Proveedor")

    qty_available_not_res = fields.Float(
        string='Quantity On Hand Unreserved',
        compute='_compute_product_available_not_res',
        search='_search_quantity_unreserved',
    )

    @api.depends('product_variant_ids.qty_available_not_res')
    def _compute_product_available_not_res(self):
        for tmpl in self:
            if isinstance(tmpl.id, models.NewId):
                continue
            tmpl.qty_available_not_res = sum(
                tmpl.mapped('product_variant_ids.qty_available_not_res')
            )

    def _search_quantity_unreserved(self, operator, value):
        domain = [('qty_available_not_res', operator, value)]
        product_variant_ids = self.env['product.product'].search(domain)
        return [('product_variant_ids', 'in', product_variant_ids.ids)]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    qty_available_not_res = fields.Float(
        string='Qty Available Not Reserved',
        compute='_compute_qty_available_not_reserved',
        search="_search_quantity_unreserved",
    )

    def _compute_product_available_not_res_dict(self):

        res = {}

        domain_quant = self._prepare_domain_available_not_reserved()
        quants = self.env['stock.quant'].with_context(lang=False).read_group(
            domain_quant,
            ['product_id', 'location_id', 'quantity', 'reserved_quantity'],
            ['product_id', 'location_id'],
            lazy=False)
        product_sums = {}
        for quant in quants:
            # create a dictionary with the total value per products
            product_sums.setdefault(quant['product_id'][0], 0.)
            product_sums[quant['product_id'][0]] += (
                quant['quantity'] - quant['reserved_quantity']
            )
        for product in self.with_context(prefetch_fields=False, lang=''):
            available_not_res = float_round(
                product_sums.get(product.id, 0.0),
                precision_rounding=product.uom_id.rounding
            )
            res[product.id] = {
                'qty_available_not_res': available_not_res,
            }
        return res

    def _prepare_domain_available_not_reserved(self):
        domain_quant = [
            ('product_id', 'in', self.ids),
        ]
        domain_quant_locations = self._get_domain_locations()[0]
        domain_quant.extend(domain_quant_locations)
        return domain_quant

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def _compute_qty_available_not_reserved(self):
        res = self._compute_product_available_not_res_dict()
        for prod in self:
            qty = res[prod.id]['qty_available_not_res']
            prod.qty_available_not_res = qty
        return res

    def _search_quantity_unreserved(self, operator, value):
        if operator not in OPERATORS:
            raise UserError(_('Invalid domain operator %s') % operator)
        if not isinstance(value, (float, int)):
            raise UserError(_('Invalid domain right operand %s') % value)

        ids = []
        for product in self.search([]):
            if OPERATORS[operator](product.qty_available_not_res, value):
                ids.append(product.id)
        return [('id', 'in', ids)]


class ProductCatgory(models.Model):
    _inherit = 'product.category'

    x_studio_por_minimo_rentabilidad = fields.Float(string='% Minimo Rentabilidad')
