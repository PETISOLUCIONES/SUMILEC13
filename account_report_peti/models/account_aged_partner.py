from odoo import models, fields, api, _


class AccountAgedPartner(models.AbstractModel):
    _inherit = 'account.aged.partner'

    def _get_columns_name(self, options):
        columns = super(AccountAgedPartner, self)._get_columns_name(options)
        columns.insert(4, {'name': _("Referencia"), 'class': '', 'style': 'text-align:center; white-space:nowrap;'})
        return columns

    # Agrega la información del detalle de la factura para el reporte
    @api.model
    def _get_lines(self, options, line_id=None):
        lines = super(AccountAgedPartner, self)._get_lines(options, line_id)
        for line in lines:
            if line['level'] == 2:
                line['columns'].insert(3, {'name': ''})
            if line['level'] == 4:
                aml = self.env['account.move.line'].search([('id', '=', line['id'])])
                referencia = aml.ref
                line['columns'].insert(3, {'name': referencia})
        return lines
