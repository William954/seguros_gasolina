# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'TVP Seguros Varios',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Agrega el modulo de control de Seguros Varios.
=============================================================

    * Tipo de Seguro
    * Prima
    * Monto Mensual
    * Proveedor

Relacionado a benefícios del empleado.
    """,
    'author': 'David Miranda',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_seguros_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,

}