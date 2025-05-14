from odoo import api, fields, models
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True)
    reference = fields.Char(string='Reference')
    date_of_birth = fields.Date(string="DOB")
    age = fields.Integer(
        string="Age",
        compute='_compute_age',
        inverse='_inverse_compute_age',
        search='_search_age',
        tracking=True
    )
    active = fields.Boolean(string="Active", default=True)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    ref = fields.Integer(string='Reference')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    description = fields.Text(string="Description")
    image = fields.Image(string="Image")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection(
        [('married', 'Married'), ('single', 'Single')],
        string="Marital Status",
        tracking=True
    )
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    def action_view_appointments(self):
        pass

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = fields.Date.context_today(self)
                dob = fields.Date.from_string(rec.date_of_birth)
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                rec.age = age
            else:
                rec.age = 0

    def _inverse_compute_age(self):
        for rec in self:
            if rec.age is not None:
                today = fields.Date.context_today(self)
                dob = today - relativedelta.relativedelta(years=rec.age)
                rec.date_of_birth = fields.Date.to_string(dob)
            else:
                rec.date_of_birth = False

    # def _search_age(self, operator, value):
    #     today = fields.Date.context_today(self)
    #     if operator == '=':
    #         dob = today - relativedelta.relativedelta(years=value)
    #         return [('date_of_birth', '=', fields.Date.to_string(dob))]
    #     elif operator == '!=':
    #         dob = today - relativedelta.relativedelta(years=value)
    #         return [('date_of_birth', '!=', fields.Date.to_string(dob))]
    #     return []

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + " (copy)"
        return super(HospitalPatient, self).copy(default)
