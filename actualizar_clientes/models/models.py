# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'


    '''def update_vat(self):
        partners = self.env['res.partner'].search([('vat_num', '=', False), ('vat', '!=', False)])
        for partner in partners:
            if partner.vat and not partner.vat_num and partner.l10n_co_document_type:
                numero = partner.GetNitCompany(partner.vat)
                if 2 < len(numero) < 12 and not re.match("^[0-9]+$", numero) is None:
                    vals = {'vat_type': partner.change_vat_type(partner), 'vat_num': numero}
                    if partner.l10n_co_document_type == 'rut':
                        dv = partner.calcular_dv(numero)
                        vals['vat_vd'] = dv
                    partner.write(vals)'''

    def update_vat(self):
        partners = self.env['res.partner'].search([('active', '=', True)])
        for partner in partners:
            if partner.l10n_co_document_type:
                partner.write({'vat_type': partner.change_vat_type(partner)})
            elif partner.vat_num:
                partner.write({'l10n_co_document_type': partner.change_vat_type_dos(partner)})


    def GetNitCompany(self, number):
        document = ''
        if '-' in number:
            document = number[0:number.find('-')]
        else:
            document = number
        return document.replace('.', '')

    def change_vat_type(self, partner):
        if partner.l10n_co_document_type == 'rut':
            return  '31'
        elif partner.l10n_co_document_type == 'id_document':
            return  '13'
        elif partner.l10n_co_document_type == 'id_card':
            return  '12'
        elif partner.l10n_co_document_type == 'passport':
            return  '41'
        elif partner.l10n_co_document_type == 'foreign_id_card':
            return '22'
        elif partner.l10n_co_document_type == 'external_id':
            return  ''
        elif partner.l10n_co_document_type == 'diplomatic_card':
            return  ''
        elif partner.l10n_co_document_type == 'residence_document':
            return  ''
        elif partner.l10n_co_document_type == 'civil_registration':
            return  '11'
        elif partner.l10n_co_document_type == 'national_citizen_id':
            return  '13'

    def change_vat_type_dos(self, partner):
        if partner.vat_type == '31':
            return  'rut'
        elif partner.vat_type == '13':
            return  'id_document'
        elif partner.vat_type == '12':
            return  'id_card'
        elif partner.vat_type == '41':
            return  'passport'
        elif partner.vat_type == '22':
            return 'foreign_id_card'
        elif partner.vat_type == '':
            return  ''
        elif partner.vat_type == '':
            return  ''
        elif partner.vat_type == '':
            return  ''
        elif partner.vat_type == '11':
            return  'civil_registration'
        elif partner.vat_type == '13':
            return  'national_citizen_id'



    def calcular_dv(self, numero):

        factor = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]
        factor = factor[-len(numero):]
        csum = sum([int(numero[i]) * factor[i] for i in range(len(numero))])
        check = csum % 11
        if check > 1:
            check = 11 - check
        return check
