# -*- coding: utf-8 -*-
# from odoo import http


# class PermisosSuper(http.Controller):
#     @http.route('/permisos_super/permisos_super/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/permisos_super/permisos_super/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('permisos_super.listing', {
#             'root': '/permisos_super/permisos_super',
#             'objects': http.request.env['permisos_super.permisos_super'].search([]),
#         })

#     @http.route('/permisos_super/permisos_super/objects/<model("permisos_super.permisos_super"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('permisos_super.object', {
#             'object': obj
#         })
