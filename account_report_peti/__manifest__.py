# -*- coding: utf-8 -*-
{
    'name': "Reporte vencidas por pagar",

    'summary': """
        Agrega el campo referencia en el reporte 
        vencidas por pagar""",

    'description': """
        Agrega el campo referencia en el reporte 
        vencidas por pagar
    """,

    'author': "PETI Soluciones Productivas",
    'website': "http://www.peti.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_reports'],

    # always loaded
    'data': [
        #'views/views.xml',
        #'views/templates.xml',
    ],

}
