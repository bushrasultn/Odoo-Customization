from odoo import fields, models


class SchoolSheet(models.Model):
    _name = "school.sheet"
    _description = "Sheets"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    _rec_name = 'session_id'

    session_id = fields.Many2one('school.session', string="Session")
    teacher_id = fields.Many2one('school.partners', string="Teacher")
    sheet_line_ids = fields.One2many('school.sheet.lines', 'school_sheet_id', string="Subjects")
    phone = fields.Char(
        string='Phone',
        related='teacher_id.contact')
    qualif = fields.Char(string='Qualification', related='teacher_id.qualification')


class SchoolSheetLines(models.Model):
    _name = 'school.sheet.lines'
    _description = "School Lines"



    subject_id = fields.Many2one('subject.school', string="Subjects")
    school_sheet_id = fields.Many2one('school.sheet', string="School Sheet")
    class_id = fields.Many2one('school.class', string="Classes")
