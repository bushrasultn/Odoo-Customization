from odoo import models, fields, api


class StudentResult(models.Model):
    _name = "student.result"
    _description = "Student Result"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Full Name', required=True)
    student_id = fields.Many2one('school.partners', string='Student', required=True)
    result = fields.Char(string='Result')
    student_name = fields.Char(related='student_id.name', string='Student Name', readonly=True)
    # subject = fields.Char(string='Subject', required=True)
    obt_marks = fields.Integer(string='Obtained Marks', required=True)
    total_marks = fields.Integer(string='Total Marks', required=True)
    percentage = fields.Float(string='Percentage', compute='_compute_percentage', store=True)
    grade = fields.Char(string='Grade', compute='_compute_grade', store=True)
    result_id = fields.Many2one('subject.school', 'Subject')
    remark = fields.Html(string='Remarks')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")

    @api.depends('obt_marks', 'total_marks')
    def _compute_percentage(self):
        for record in self:
            if record.total_marks:
                record.percentage = (record.obt_marks / record.total_marks) * 100
            else:
                record.percentage = 0.0

    @api.depends('percentage')
    def _compute_grade(self):
        for record in self:
            if record.percentage >= 100:
                record.grade = 'A'
            elif record.percentage >= 80:
                record.grade = 'B'
            elif record.percentage >= 60:
                record.grade = 'C'
            else:
                record.grade = 'D'
