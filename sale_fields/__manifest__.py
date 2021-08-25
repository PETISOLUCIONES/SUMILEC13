# -*- coding: utf-8 -*-
{
    'name': "sale_campos",

    'summary': """
        Agrega campos""",

    'description': """
        Agrega campos
    """,

    'author': "PETI Soluciones Productivas",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'sale_management'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/res_partner.xml',
        'views/product_template.xml',
        'report/sale_report.xml',
    ],
    'qweb': ['static/src/xml/qty_at_date.xml'],

}
