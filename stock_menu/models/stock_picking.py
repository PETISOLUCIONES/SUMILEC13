# -*- coding: utf-8 -*-

from odoo import models, fields, api



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_city = fields.Char(related='partner_id.city', string='Ciudad', readonly=True, store=True)
    partner_address = fields.Char(related='partner_id.street', string='Dirección', readonly=True, store=True)
    partner_state = fields.Char(related='partner_id.state_id.name', string='Departamento', readonly=True, store=True)
    seller_name = fields.Char(related='partner_id.user_id.name', string='Vendedor', readonly=True, store=True)
    partner_nit = fields.Char(related='partner_id.vat', string='NIT', readonly=True, store=True)
    purchase_id = fields.Many2one('purchase.order', related='move_lines.purchase_line_id.order_id', string='Pedidos de compra', readonly=True)
    sale_id = fields.Many2one('sale.order', related='group_id.sale_id', string='Pedidos de venta', readonly=True)
    '''estado_so = fields.Selection(	[['draft', 'Cotizacion'],
                                      ['sent', 'Cotizacion Enviada'],
                                      ['credit_limit', 'Limite de Credito'],
                                      ['sale', 'Orden de Venta'],
                                      ['done', 'Bloqueado'],
                                      ['cancel', 'Cancelado']],
                             string='Estado SO', related='sale_id.state', readonly=True, store=True)'''
    #estado_so = fields.Char(string='Estado SO', related='sale_id.state.value', readonly=True, store=True)
    total_orden = fields.Monetary(string='Total orden', related='sale_id.amount_total')
    total_su = fields.Float(string='Total SU', compute='_get_total_su')
    plazo_pago = fields.Char(string='Plazo de pago', related='sale_id.payment_term_id.name', store=True)
    factura_relacionada = fields.Char(string='Factura relacionada', related='sale_id.facturas_relacionadas', store=True)
    estado_factura = fields.Selection([('upselling', 'Oportunidad de Sobreventa'),
                                       ('invoiced', 'Facturado'),
                                       ('to invoice', 'Para Facturar'),
                                       ('no', 'Nada para Facturar')], string='Estado Factura (FV)', related='sale_id.invoice_status', store=True, readonly=True)
    tipo_entrega = fields.Selection([("Ventas Mostrador","Ventas Mostrador"),
                                     ("Despacho Normal","Despacho Normal")], string='Tipo de entrega')
    estado = fields.Selection([["En espera de material","En espera de material"],
                               ["Impreso","Sin Estado "],
                               ["ESTADO","En alistamiento"],
                               ["Separado","Separado"],
                               ["Empacado o (para guia)","Empacado o (para guia)"],
                               ["No aplica para flete","No aplica para flete"],
                               ["Terminado","Terminado"],
                               ["Espera de Formulario","Espera de Formulario"],
                               ["En espera de fecha de confirmación de despacho","En espera de fecha de confirmación de despacho"]], string='Estado de alistamiento', track_visibility='onchange', copy=False)
    empresa_transpostadora = fields.Selection([["Servientrega","Servientrega"],
                                               ["coordinadora","Coordinadora"],
                                               ["Envía","Envía"],
                                               ["Transprensa","Transprensa"],
                                               ["Transporte Propio","Transporte Propio"],
                                               ["Trasportado o recogido por el cliente","Transportado o Recogido por el cliente"],
                                               ["Otro","Otro"]],
                                              string='Tipo de transporte', track_visibility='onchange', copy=False)
    unidades = fields.Float(string='Unidades', copy=False)
    peso_kg = fields.Float(string='Peso (Kg)', copy=False)
    volumen = fields.Float(string='Volumen', copy=False)
    fecha_hora_envio = fields.Datetime(string='Fecha y Hora de Envio', track_visibility='onchange', copy=False)
    numero_guia = fields.Char(string='Numero de guia', track_visibility='onchange', copy=False)
    empacado_por = fields.Char(string='Empacado Por', track_visibility='onchange', copy=False)
    total_productos = fields.Monetary(string='Total Productos', compute='_get_total_productos')
    mano_obra = fields.Monetary(string='Mano de obra')
    total_produccion = fields.Monetary(string='Total Produccion', compute='_get_total_production')
    es_produccion = fields.Boolean(string='Es producción')
    orden_produccion = fields.Many2one('stock.picking', string='Orden de producción')
    currency_id = fields.Many2one(
        string="Currency", related="company_id.currency_id", readonly=True
    )



    @api.depends('mano_obra')
    def _get_total_production(self):
        for record in self:
            record['total_produccion'] = record.total_productos + record.mano_obra

    @api.depends('move_ids_without_package')
    def _get_total_productos(self):
        total = 0
        for record in self:
            for m in record.move_ids_without_package:
                total += m.costo_total
            record['total_productos'] = total


    @api.depends('move_ids_without_package')
    def _get_total_su(self):
        total = 0
        for record in self:
            for linea in record.move_ids_without_package:
                for venta in record.sale_id.order_line:
                    if linea.product_id.id == venta.product_id.id:
                        total += venta.price_total
            record['total_su'] = total

    '''@api.model
    def create(self, vals):
        if 'backorder_id' in vals:
            data = [vals.pop(key, None) for key in ['empresa_transpostadora', 'unidades',
                                              'peso_kg', 'volumen',
                                              'fecha_hora_envio', 'numero_guia',
                                              'empacado_por']]
        return super(StockPicking, self).create(vals)'''

class StockMove(models.Model):
    _inherit = 'stock.move'

    costo_total = fields.Float(string='Costo total', compute='_get_costo_total')
    costo = fields.Float(string='Costo', related='product_id.standard_price')

    @api.depends('costo')
    def _get_costo_total(self):
        for record in self:
            record['costo_total'] = record.product_uom_qty * record.costo

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    facturas_relacionadas = fields.Char(string='Factura relacionada', related='invoice_ids.name', readonly=True)

