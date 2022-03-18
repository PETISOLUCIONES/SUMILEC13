# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


#Verifica si una linea del reporte tiene la información de los vendedores
# seleccionados
def validaLinea( x, sellers):
    valido = False
    if x['level'] == 2 :
        valido = True
    if x['level'] == 4 and x['columns'][4]['name'] in sellers:
        valido = True
    return valido
class report_account_aged_partner(models.AbstractModel):
    _inherit = 'account.aged.partner'

    filter_partner = True
    filter_seller = True



    #Agrega la información del detalle de la factura para el reporte
    @api.model
    def _get_lines(self, options,line_id=None):
        lines = super(report_account_aged_partner, self)._get_lines(options,line_id)
        #Recorre las lineas de detalles del reporte y agrega un espacio en blanco
        #para las de titulo (level = 2) y agrega el dato del vendedor en las de
        #detalle (level = 4)
        #Filtra las lineas por el vendedor seleccionado
        ctx = self._context
        sellers = []
        if 'seller_ids' in ctx:
            if ctx['seller_ids']:
                sellers = ctx['seller_ids'].ids
        partners = []
        sellersname = []

        for line in lines:
            if line['level'] == 2:
                line['columns'].insert(4, {'name': ''})
            if line['level'] == 4:
                vendedormod = self.env['account.move.line'].search([('id', '=', line['id'])])
                vendedor = vendedormod.move_id.user_id.name
                vendedor_id = vendedormod.move_id.user_id.id
                #cuando por el tipo de pago no trae información del vendedor
                if not(vendedor) and vendedormod.ref:
                    vendedorotro = self.env['account.move'].search([('name', '=', vendedormod.ref)])
                    vendedor = vendedorotro.user_id.name
                    vendedor_id = vendedorotro.user_id.id
                #agrega los datos de partners
                if sellers and vendedor_id in sellers:
                    sellersname.append(vendedor)
                line['columns'].insert(4, {'name': vendedor})
        lineas = []
        if sellers :
            lineas = [elemento for elemento in lines if validaLinea(elemento,sellersname)]
        else:
            lineas = lines
        return lineas

    #Agrega la columna de Vendedor para el informe
    def _get_columns_name(self, options):
        columns = super(report_account_aged_partner, self)._get_columns_name(options)
        #columns.append({'name': _("Vendedor"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'})
        columns.insert(5,{'name': _("Vendedor"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'})
        return columns

class account_report(models.AbstractModel):
    _inherit = 'account.report'
    filter_seller= None

    @api.model
    def _init_filter_seller(self, options, previous_options=None):
        if not self.filter_seller:
            return

        options['seller'] = True
        options['seller_ids'] = previous_options and previous_options.get(
            'seller_ids') or []
        selected_seller_ids = [int(seller) for seller in options['seller_ids']]
        selected_sellers = selected_seller_ids and self.env['res.users'].browse(selected_seller_ids) or self.env['res.users']
        options['selected_seller_ids'] = selected_sellers.mapped('name')


    def _set_context(self, options):
        """This method will set information inside the context based on the options dict as some options need to be in context for the query_get method defined in account_move_line"""
        ctx = super(account_report, self)._set_context(options)
        if options.get('seller_ids'):
            ctx['seller_ids'] = self.env['res.users'].browse([int(partner) for partner in options['seller_ids']])

        return ctx

class report_account_report_agedpartnerbalance(models.AbstractModel):
    _inherit = 'report.account.report_agedpartnerbalance'
    #heredamos para modificar las lineas y filtros si se escogió vendedores
    def _get_partner_move_lines(self, account_type, date_from, target_move, period_length):
        res, total, lines = super(report_account_report_agedpartnerbalance, self)._get_partner_move_lines(account_type, date_from, target_move, period_length)
        ctx = self._context
        sellers = []
        partners = []
        resfiltrado = res
        totalfiltrado  = total
        lineseliminar = []

        if 'seller_ids' in ctx:
            if ctx['seller_ids']:
                sellers = ctx['seller_ids'].ids
                #Crea una lista de partners
                for partner  in lines:
                    lineseliminar = []
                    for line in lines[partner]:
                        vendedormod = self.env['account.move.line'].search(
                            [('id', '=', line['line']['id'])])
                        vendedor = vendedormod.move_id.user_id.id
                        if not (vendedor) and vendedormod.ref:
                            vendedorotro = self.env['account.move'].search(
                                [('name', '=', vendedormod.ref)])
                            vendedor = vendedorotro.user_id.id
                        if vendedor in sellers:
                            partners.append(line['line']['partner_id'].id)
                            continue
                        else:
                          lineseliminar.append(line)
                    for x in lineseliminar:
                        lines[partner].remove(x)

                resfiltrado = [x for x in res if (x['partner_id'] in partners)]
                for elem in resfiltrado:
                    totalres = 0.0
                    for i in range(5):
                        elem[str(i)] = sum( x['amount'] for x in lines[elem['partner_id']] if(x['period'] -1  == i))
                        totalres += elem[str(i)]
                    elem['direction'] = sum( x['amount'] for x in lines[elem['partner_id']] if(x['period']   == 6))
                    totalres += elem['direction']
                    elem['total'] = totalres
                if resfiltrado:
                    for i in (4,3,2,1,0):
                        total[i] = sum(x[str(i)] for x in resfiltrado)
                    total[5] = sum(x['total'] for x in resfiltrado)
                    total[6] = sum(x['direction'] for x in resfiltrado)
                    if total[5] == 0:
                        total = []
                else:
                    total = []



        return resfiltrado, total, lines



