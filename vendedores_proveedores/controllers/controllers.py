# -*- coding: utf-8 -*-
# from odoo import http


# class VendedorEmpleado(http.Controller):
#     @http.route('/vendedor_empleado/vendedor_empleado/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vendedor_empleado/vendedor_empleado/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vendedor_empleado.listing', {
#             'root': '/vendedor_empleado/vendedor_empleado',
#             'objects': http.request.env['vendedor_empleado.vendedor_empleado'].search([]),
#         })

#     @http.route('/vendedor_empleado/vendedor_empleado/objects/<model("vendedor_empleado.vendedor_empleado"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vendedor_empleado.object', {
#             'object': obj
#         })
