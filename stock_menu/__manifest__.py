# -*- coding: utf-8 -*-
{
    'name': "stock_menu",

    'summary': """
        Reemplazar el metodo para  visualizar las transferencias de inventario""",

    'description': """
        Reemplazar el metodo para  visualizar las transferencias de inventario
    """,

    'author': "PETI Soluciones Productivas",
    'website': "http://www.peti.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'sale', 'sale_stock', 'purchase', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/stock_picking_view.xml',
        'views/stock_move.xml',
        'report/report_picking.xml',
    ],

}
