# coding: utf-8
from lxml import etree

from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ResPartner, self).fields_view_get(view_id=view_id,
                                                      view_type=view_type,
                                                      toolbar=toolbar,
                                                      submenu=submenu)
        user_id = self.env.user.id
        access_partner = False
        user_master_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'user_master')[1]
        user_partner_id = self.env['ir.model.data'].get_object_reference('permisos_super', 'access_contacts')[1]
        #sale_user_id = self.env['ir.model.data'].get_object_reference('sales_team', 'group_sale_salesman')[1]
        #sales_all_user_id = self.env['ir.model.data'].get_object_reference('sales_team', 'group_sale_salesman_all_leads')[1]
        #stock_user_id = self.env['ir.model.data'].get_object_reference('stock', 'group_stock_user')[1]
        browse_group = self.env['res.groups'].search(
            [('id', 'in', [user_master_id, user_partner_id])])
        list_user = []
        for user in browse_group.users:
            list_user.append(user.id)
        if user_id in list_user:
            access_partner = True

        if not access_partner:
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//form'):
                    node.set('create', 'false')
                    node.set('edit', 'false')
                res['arch'] = etree.tostring(doc)
            elif view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//tree'):
                    node.set('create', 'false')
                res['arch'] = etree.tostring(doc)
            elif view_type == 'kanban':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//kanban'):
                    node.set('create', 'false')
                res['arch'] = etree.tostring(doc)
        return res
