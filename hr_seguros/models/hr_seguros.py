# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

#Boton de Seguros (editar despues de clase de tarjetas)

class Employee(models.Model):

    _inherit = "hr.employee"

    seguros_id = fields.Many2one('hr.seguros', compute='_compute_seguros_id', string='Seguros', help='Seguros Varios')
    seguros_count = fields.Integer(compute='_compute_seguros_count', string='Seguros')

    def _compute_seguros_id(self):
        """ Ir a la tarjeta de Seguros """
        Seguros = self.env['hr.seguros']
        for employee in self:
            employee.seguros_id = Seguros.search([('employee_id', '=', employee.id)], limit=1)

    def _compute_seguros_count(self):
        # Contador de Seguros
        seguros_data = self.env['hr.seguros'].sudo().read_group([('employee_id', 'in', self.ids)], ['employee_id'], ['employee_id'])
        result = dict((data['employee_id'][0], data['employee_id_count']) for data in seguros_data)
        for employee in self:
            employee.seguros_count = result.get(employee.id, 0)

#Módulo de control de Seguros

class Seguros(models.Model):

    _name = 'hr.seguros'
    _description = 'Seguros Varios'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('No. de Seguro o Tarjeta', required=True)
    active = fields.Boolean(default=True)
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    department_id = fields.Many2one('hr.department', string="Departamento")
    job_id = fields.Many2one('hr.job', string='Job Position')
    prima_neta = fields.Float(string='Prima Neta')
    derecho_poliza = fields.Float(string='Derecho de Póliza')
    proveedor_id = fields.Many2one('res.partner', string='Proveedor')
    vigencia_meses = fields.Integer('Vigencia en Meses', default="12", help="Duración del Seguro")
    fecha_inicio = fields.Date('Fecha de inicio')
    fecha_vencimiento = fields.Date('Vencimiento')
    tipo_seguro = fields.Selection([
        ('segvida', 'Seguro de Vida'),
        ('seggmm', 'Gastos Médicos Mayores')], string='Tipo de Seguro')
    tipo_moneda = fields.Selection([
        ('mxn', 'MXN'),
        ('dll', 'Dll')], string='Moneda')
    state = fields.Selection([
        ('asignado', 'Asignado'),
        ('porvencer', 'Por vencer'),
        ('vencido', 'Vencido'),
        ('cancelado', 'Cancelado')], string='Status', track_visibility='onchange', help='Status of the contract', default='asignado')
    active = fields.Boolean('Archivar', default=True)
    notes = fields.Text('Notes')

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id
            self.department_id = self.employee_id.department_id
