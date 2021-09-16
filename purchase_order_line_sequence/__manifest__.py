# -*- coding: utf-8 -*-
{
    'name': "Secuencia Compra",

    'summary': """
        Agrega campo de secuencia en compras""",

    'description': """
        Agrega campo de secuencia en compras
    """,

    'author': "PETI SOluciones Productivas",
    'website': "http://www.peti.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        'views/purchase_order_view.xml',
        'views/report_purchase.xml',
    ],

}
