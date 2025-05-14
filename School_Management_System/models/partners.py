from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _name = "school.partners"
    _description = "Partners"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    father_name = fields.Char(string='Father Name')
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')
    date_of_birth = fields.Date(string="DOB")
    contact = fields.Char(string="Mobile Number", tracking=True)
    is_teacher = fields.Boolean(string='Is Teacher', default=False)
    is_student = fields.Boolean(string='Is Student', default=True)
    admission_date = fields.Date(string="Admission Date")
    reference = fields.Char(string="Reference", default='New')
    note = fields.Text(string="Description")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='draft')
    admission_time = fields.Datetime(string='Admission Time')
    cnic = fields.Char(string='CNIC Number', size=15)
    qualification = fields.Char(string='Qualification')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", tracking=True)
    teacher_id = fields.Many2one('school.sheet', string='Teacher')
    student_id = fields.Many2one('student.result', string='Student')
    student_fee_id = fields.Many2one('fee.fee')

    image = fields.Image(string="Image")
    # admission_count = fields.Integer(string='Admission Count', compute='_compute_admission_count')
    #
    # @api.depends(admission_count)
    # def _compute_admission_count(self):
    #     for rec in self:
    #         rec.admission_count = len(rec.admission_count)
    #
    # def action_view_admission(self):
    #     pass

    @api.model
    def create(self, vals):
        id_num = vals.get('id_num')
        contact = vals.get('contact')

        if id_num:
            if len(id_num) == 13:
                province = id_num[:5]
                family = id_num[5:12]
                gender = id_num[12:]
                cnic = f"{province}-{family}-{gender}"
                vals['id_num'] = cnic
            else:
                raise ValidationError('CNIC should be 13 digits!')

        if contact:
            if len(contact) != 11:
                raise ValidationError('Contact number should be 11 digits!')

        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('school.partners') or 'New'

        return super(Partner, self).create(vals)

    def write(self, vals):
        id_num = vals.get('id_num')

        if id_num:
            if '-' in id_num:
                if len(id_num) == 13:
                    province = id_num[:5]
                    family = id_num[5:12]
                    gender = id_num[12:]
                    cnic = f"{province}-{family}-{gender}"
                    vals['id_num'] = cnic
        return super(Partner, self).write(vals)


