from lxml import etree
import json
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductTemplate, self).fields_view_get(view_id=view_id,
                                                           view_type=view_type,
                                                           toolbar=toolbar,
                                                           submenu=submenu)
        user_id = self.env.user.id
        access_product = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        group_purchase_user_id = self.env['ir.model.data'].get_object_reference('purchase', 'group_purchase_user')[1]
        group_purchase_manager_id = \
            self.env['ir.model.data'].get_object_reference('purchase', 'group_purchase_manager')[1]
        browse_group = self.env['res.groups'].search(
            [('id', 'in', [user_master_id, group_purchase_user_id, group_purchase_manager_id])])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_product = True

        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if not access_product:
                for node in doc.xpath('//form'):
                    node.set('create', 'false')
                    node.set('edit', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'tree' and not access_product:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//tree'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'kanban' and not access_product:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//kanban'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        return res

    def actualizar_costo(self):
        user_id = self.env.user.id
        access_product = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        browse_group = self.env['res.groups'].search(
            [('id', '=', user_master_id)])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_product = True
        return access_product


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductProduct, self).fields_view_get(view_id=view_id,
                                                          view_type=view_type,
                                                          toolbar=toolbar,
                                                          submenu=submenu)
        user_id = self.env.user.id
        access_product = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        group_purchase_user_id = self.env['ir.model.data'].get_object_reference('purchase', 'group_purchase_user')[1]
        group_purchase_manager_id = \
        self.env['ir.model.data'].get_object_reference('purchase', 'group_purchase_manager')[1]
        browse_group = self.env['res.groups'].search(
            [('id', 'in', [user_master_id, group_purchase_user_id, group_purchase_manager_id])])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_product = True

        if view_type == 'form':
            doc = etree.XML(res['arch'])
            if not access_product:
                for node in doc.xpath('//form'):
                    node.set('create', 'false')
                    node.set('edit', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'tree' and not access_product:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//tree'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        elif view_type == 'kanban' and not access_product:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//kanban'):
                node.set('create', 'false')
            res['arch'] = etree.tostring(doc)
        return res

    def actualizar_costo(self):
        user_id = self.env.user.id
        access_product = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        browse_group = self.env['res.groups'].search(
            [('id', 'in', [user_master_id])])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_product = True
        return access_product


class StockChangeStandardPrice(models.TransientModel):
    _inherit = 'stock.change.standard.price'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(StockChangeStandardPrice, self).fields_view_get(view_id=view_id,
                                                                    view_type=view_type,
                                                                    toolbar=toolbar,
                                                                    submenu=submenu)

        user_id = self.env.user.id
        access_product = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        browse_group = self.env['res.groups'].search(
            [('id', 'in', [user_master_id])])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_product = True

        if view_type == 'form' and not access_product:
            doc = etree.XML(res['arch'])
            '''for node in doc.xpath('//form/footer/button[1]'):
                node.set("invisible", "1")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['invisible'] = True
                node.set("modifiers", json.dumps(modifiers))'''
            for node in doc.xpath("//field[@name='new_price']"):
                node.set("readonly", "1")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['readonly'] = True
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(PurchaseOrder, self).fields_view_get(view_id=view_id,
                                                         view_type=view_type,
                                                         toolbar=toolbar,
                                                         submenu=submenu)
        user_id = self.env.user.id
        access_invoice = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        group_account_manager_id = self.env['ir.model.data'].get_object_reference('account', 'group_account_manager')[1]
        browse_group = self.env['res.groups'].search(
            [('id', 'in', [user_master_id, group_account_manager_id])])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_invoice = True

        if view_type == 'form' and not access_invoice:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//form/header/button[11]'):
                node.set("invisible", "1")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['invisible'] = True
                node.set("modifiers", json.dumps(modifiers))
            for node in doc.xpath('//form/header/button[6]'):
                node.set("invisible", "1")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['invisible'] = True
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(SaleOrder, self).fields_view_get(view_id=view_id,
                                                     view_type=view_type,
                                                     toolbar=toolbar,
                                                     submenu=submenu)
        user_id = self.env.user.id
        access_invoice = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        group_account_manager_id = self.env['ir.model.data'].get_object_reference('account', 'group_account_manager')[1]
        browse_group = self.env['res.groups'].search(
            [('id', 'in', [user_master_id, group_account_manager_id])])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_invoice = True

        if view_type == 'form' and not access_invoice:
            doc = etree.XML(res['arch'])
            for node in doc.xpath('//form/header/button[4]'):
                node.set("invisible", "1")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['invisible'] = True
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res
