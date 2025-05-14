from odoo import api, fields, models


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name = fields.Char(string='Operation Name')
    reference_record = fields.Reference([('hospital.patient', 'Patient')], string="Record")

    @api.model
    def name_created(self, name):
        record = self.create({'operation_name': name})
        return record.name_get()[0][1]
