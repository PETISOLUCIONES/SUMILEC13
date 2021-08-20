# -*- coding: utf-8 -*-
{
    'name': "Descripción en Factura",

    'summary': """
        Añade la descripción en las facturas de proveedores
        cuando existe una diferencia de pago""",

    'description': """
        Añade la descripción en las facturas de proveedores
        cuando existe una diferencia de pago.
    """,

    'author': "PETI Soluciones Productivas",
    'website': "https://peti.com.co",

    'category': 'Uncategorized',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],

    # always loaded
    'data': [
        'reports/report_invoice_document_with_description.xml',
    ],
}
