# -*- coding: utf-8 -*-

from odoo import api, models, fields, exceptions


# Clientes
class ResPartner(models.Model):
    _inherit = "res.partner"

    def cadena(self):
        domain = "['|',('department_id','ilike', 'Comercial'), ('department_id','ilike', 'ventas')]"
        return domain

    # campo con el id de los vendedores relacionado con hr_employee
    vendedores_autorizados_id = fields.Many2many(comodel_name='hr.employee',
                                                 relation='vendedores_provedores_ids',
                                                 domain=cadena,
                                                 store=True,
                                                 string='Vendedores autorizados',
                                                 )


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def search_productos_vendedor_app(self):
        prod = []

        proveedores = self.env["res.partner"].search([("vendedores_autorizados_id", "in", self.id)])
        proveedores = proveedores.mapped("id")
        for id in proveedores:
            productos_idApp = self.env["product.supplierinfo"].search([("name", "=", id)]).product_tmpl_id
            for idProduct in productos_idApp.product_variant_ids.mapped('id'):
                if not idProduct in prod:
                    prod.append(idProduct)

        return prod
