# -*- coding: utf-8 -*-

from odoo import models


class UpdateSellerCode(models.Model):
    _name = 'update.seller.code'

    def do_update(self):
        res = self.env['product.template'].search([])
        for r in res:
            if r.seller_ids and r.seller_ids[0].product_code:
                r.product_seller_code = r.seller_ids[0].product_code
                r.seller_ids[0].product_code = None
