from odoo import models, fields


class TeacherAdminWizard(models.TransientModel):
    _name = "teacher.admin.wizard"
    _description = "Teacher Administration Wizard"

    partners_id = fields.Many2one('school.partners', string="Partners")
    cnic = fields.Char(string="CNIC")
    dob = fields.Date(string="DOB")

    def action_update_report(self):
        if self.partners_id:
            self.partners_id.write({
                'date_of_birth': self.dob,
                'cnic': self.cnic
            })

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
