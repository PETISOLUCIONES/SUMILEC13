# -*- coding: utf-8 -*-
{
    'name': "Corrección en unidades de devolución",

    'summary': """
        Evita el retorno de productos en las SO al realizar un ajuste.""",

    'description': """
        Las facturas rectificativas no descuentan la cantidad de productos en 
        las ordenes de venta cuando el precio de retorno es diferente al 
        precio de venta.
    """,

    'author': "PETI Soluciones Productivas",
    'website': "https://peti.com.co",

    'category': 'Uncategorized',
    'version': '13.1',

    'depends': [
        'base',
        'sale',
        'account',
    ],

    'data': [
        'views/account_move_view.xml',
    ],
}
