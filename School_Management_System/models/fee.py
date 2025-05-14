from odoo import models, fields, api


class StudentFee(models.Model):
    _name = 'student.fee'
    _description = 'Student Fees'

    class_id = fields.Many2one('school.class', string="Class", required=True)
    session_id = fields.Many2one('school.session', string="Session", required=True)
    date = fields.Date(string="Submit Date", required=True)
    month = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string='Month')
    fee = fields.Float(string='Fee')
    number_of_students = fields.Integer(string='Number of Students', default=1)
    student_line_ids = fields.One2many('fee.record', 'student_fee_id', string="Fee Records")
    color = fields.Integer(string="Color")

    def action_calculate_fees(self):
        for record in self:
            record._compute_fees()

    @api.depends('student_line_ids.amount')
    def _compute_fees(self):
        for record in self:
            record.total_fee = sum(line.amount for line in record.student_line_ids)


class FeeRecord(models.Model):
    _name = 'fee.record'
    _description = 'Fee Record'

    student_fee_id = fields.Many2one('student.fee', string='Student Fee', required=True)
    student_id = fields.Many2one('school.partners', string='Student', required=True)
    date = fields.Date(string='Date')
    amount = fields.Float(string='Fee')
