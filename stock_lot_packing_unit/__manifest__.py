# -*- coding: utf-8 -*-
{
    'name': "Unidad de empaque Lote",

    'summary': """
        Unidad de empaque en el lote """,

    'description': """
        Agrega el campo unidad de empaque en los lotes y 
        permite genera un nuevo lote con las cantidades 
        restantes cada que no se cumpla con la cantidad de empaque establecida 
        en el lote al generar una orden de salida
    """,

    'author': "PETI Soluciones Productivas",
    'website': "http://www.peti.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
