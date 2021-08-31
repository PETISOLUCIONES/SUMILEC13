# -*- coding: utf-8 -*-

from odoo import models


class UpdateRentabilidad(models.Model):
    _name = 'update.rentabilidad'

    def do_update(self):
        res = self.env['account.move'].search([('type', '=', 'out_invoice'), ('x_studio_rentabilidad', '=', None)])
        for r in res:
            r._compute_costo_total()
            r._compute_rentabilidad()
            r._compute_studio_rentabilidad_por()

