# -*- coding: utf-8 -*-
{
    'name': "Permisos",

    'summary': """
        Otorga diferentes permisos solo a administradores o SU""",

    'description': """
        Otorga diferentes permisos solo a administradores o SU
    """,

    'author': "PETI Soluciones Productivas",
    'website': "http://www.peti.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'calendar', 'account', 'sale_margin', 'purchase', 'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        'security/security.xml',
    ],

}
