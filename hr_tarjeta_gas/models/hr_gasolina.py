# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

#Boton de Gasolina (editar despues de clase de tarjetas)

class Employee(models.Model):

    _inherit = "hr.employee"

    gasolina_id = fields.Many2one('hr.gasolina', compute='_compute_gasolina_id', string='Gasolina', help='Tarjeta Asignada')
    gasolina_count = fields.Integer(compute='_compute_gasolina_count', string='Gasolina')

    def _compute_gasolina_id(self):
        """ Ir a la tarjeta de gas """
        Gasolina = self.env['hr.gasolina']
        for employee in self:
            employee.gasolina_id = Gasolina.search([('employee_id', '=', employee.id)], limit=1)

    def _compute_gasolina_count(self):
        # Contador de Tarjetas Asignadas
        gasolina_data = self.env['hr.gasolina'].sudo().read_group([('employee_id', 'in', self.ids)], ['employee_id'], ['employee_id'])
        result = dict((data['employee_id'][0], data['employee_id_count']) for data in gasolina_data)
        for employee in self:
            employee.gasolina_count = result.get(employee.id, 0)

#Módulo de control de Tarjeta de Gas

class Gasolina(models.Model):

    _name = 'hr.gasolina'
    _description = 'Gasolina'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('No. Tarjeta', required=True)
    active = fields.Boolean(default=True)
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    department_id = fields.Many2one('hr.department', string="Departamento")
    job_id = fields.Many2one('hr.job', string='Job Position')
    monto_mensual = fields.Float(string='Monto Mensual')
    monto_anual = fields.Float(string='Monto Anual')
    proveedor_id = fields.Many2one('res.partner', string='Proveedor')
    active = fields.Boolean('Tarjeta Activa', default=True)
    notes = fields.Text('Notes')

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id
            self.department_id = self.employee_id.department_id

    @api.onchange('monto_mensual')
    def _onchange_monto_mensual(self):
            self.monto_anual = self.monto_mensual * 12
