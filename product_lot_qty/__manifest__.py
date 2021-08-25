# -*- coding: utf-8 -*-
{
    'name': "Cantidad de Productos en Lote",

    'summary': """
        Agregar columnas a la vista tree donde se muestra la cantidad de productos""",

    'description': """
        Agregar columnas a la vista tree donde se muestra la cantidad de productos
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
        'views/views.xml',
    ],

}
