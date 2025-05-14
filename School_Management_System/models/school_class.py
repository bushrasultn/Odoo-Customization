from odoo import fields, models


class SchoolClass(models.Model):
    _name = "school.class"
    _description = "School Class"

    name = fields.Char(string='Class Name')
    section = fields.Integer(string='Section')
    # class_ids = fields.Many2one('school.sheet', 'class_id')
    # fee_ids = fields.One2many('student.fee', 'class_id', string='Class')
    active = fields.Boolean(string='Active', default=True)

    def action_new(self):
        print("Button Clicked!")
        return True
