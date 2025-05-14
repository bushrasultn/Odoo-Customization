from odoo import fields, models, api


class SchoolSubject(models.Model):
    _name = "subject.school"
    _description = "Subject"

    name = fields.Char(string='Subject Name')
    code = fields.Char(string='Subject Code')
    sheet_id = fields.Many2one('school.sheet')
    result_id = fields.Many2one('student.result', string="Subject")

    def action_test(self):
        action = {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': 'https://www.odoo.com/'
        }
        return action

