# -*- coding: utf-8 -*-
{
    'name': "vendedorProveedor",

    'summary': """
            El campo vendedor en clientes, se carga desde empleados y no de usuarios.""",

    'description': """
        El campo vendedor en clientes se cargará de empleado que sea tipo ventas y no de usuarios.
    """,

    'author': "PETI Soluciones Productivas",
    'website': "http://www.peti.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
