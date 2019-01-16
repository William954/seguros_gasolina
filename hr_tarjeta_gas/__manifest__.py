# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'TVP Tarjetas de Gasolina',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Agrega el modulo de control de tarjetas de gasolina.
=============================================================

    * Numero de tarjeta
    * Monto Anual
    * Monto Mensual
    * Proveedor

Relacionado a benefícios del empleado.
    """,
    'author': 'David Miranda',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_gasolina_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,

}
