from odoo import fields, models, api

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    name = fields.Text(string="Reason")
    cancel = fields.Date(string="Cancel Date")

    def action_cancel(self):
        cancel_days = int(self.env['ir.config_parameter'].get_param('hn_hospital.cancel_days', default=0))
        if self.appointment_id:
            self.appointment_id.state = 'cancel'

        query = "SELECT id AS patient_id FROM hospital_appointment"
        self.env.cr.execute(query)
        patients = self.env.cr.dictfetchall()
        print(patients)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        return res
