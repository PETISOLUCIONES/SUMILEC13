# -*- coding: utf-8 -*-
# from odoo import http


# class SellerReportAgedCartera(http.Controller):
#     @http.route('/seller_report_aged_cartera/seller_report_aged_cartera/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/seller_report_aged_cartera/seller_report_aged_cartera/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('seller_report_aged_cartera.listing', {
#             'root': '/seller_report_aged_cartera/seller_report_aged_cartera',
#             'objects': http.request.env['seller_report_aged_cartera.seller_report_aged_cartera'].search([]),
#         })

#     @http.route('/seller_report_aged_cartera/seller_report_aged_cartera/objects/<model("seller_report_aged_cartera.seller_report_aged_cartera"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('seller_report_aged_cartera.object', {
#             'object': obj
#         })
