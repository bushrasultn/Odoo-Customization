from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta


class FormulationInfo(models.Model):
    _name = 'formulation.info'
    _description = 'Formulation and Manufacturer Information'

    pest_id = fields.Many2one('pesticides.reg', string="Pesticides Registration")
    formulation = fields.Many2one('form.reg', string="Formulation")
    mnf_name = fields.Char(string='Manufacturer')
    license_no = fields.Char(string='MNF License No.')


class TechnicalInfo(models.Model):
    _name = 'technical.info'
    _description = 'Technical and Manufacturer Information'

    pest_id = fields.Many2one('pesticides.reg', string="Pesticides Registration")
    technical = fields.Char(string="Technical %")
    mnf_name = fields.Char(string='Manufacturer')
    license_no = fields.Char(string='MNF License No.')


class PesticidesReg(models.Model):
    _name = 'pesticides.reg'
    _description = 'Pesticides Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(default=lambda rec: 'New')
    sequence = fields.Char(string='Code', default='New')
    sr_no = fields.Char(string="Serial #", default='New')
    ref_no = fields.Char(string="Reference #", Tracking=True)
    product = fields.Many2one('product.product',
                              string='Product Name', Tracking=True)
    brand = fields.Char(string="Brand Name", Tracking=True)
    generic = fields.Char(string="Common Name", Tracking=True)
    form_type = fields.Many2one('form.type',
                                string="Form Type", Tracking=True)
    undertaking = fields.Many2one('name.undertaking',
                                  string="Name Undertaking", Tracking=True)
    reg_date = fields.Date(string="Registration Date", Tracking=True)
    expiry_date = fields.Date(string="Expiry Date", Tracking=True)
    alert = fields.Selection(
        [('none', 'None'), ('imp', 'Important'), ('urgent', 'Urgent')],
        string='Alert', compute="_compute_alert", store=True)
    apply_date = fields.Date(string="Renewal Apply Date", Tracking=True)
    renewal_date = fields.Date(string="Renewal Receive Date", Tracking=True)
    province = fields.Many2one('province.reg',
                               string='Province/Department', Tracking=True)
    country = fields.Many2one('origin.reg',
                              string="Country of Origin", Tracking=True)
    crops = fields.Char(string="Use of Crops", Tracking=True)
    category = fields.Many2one('category.name',
                               string='Category', Tracking=True)
    exp_agent = fields.Char(string="Export Agent")
    ref_agent = fields.Char(string="Reference Agent")
    state = fields.Selection(
        [('draft', 'Draft'), ('applied', 'Applied'),
         ('registered', 'Registered'), ('expired', 'Expired'),
         ('renewal', 'Renewal'), ], string='State',
        default='draft', Tracking=True)
    formulation_lines = fields.One2many('formulation.info', 'pest_id',
                                        string="Formulation Info")
    technical_lines = fields.One2many('technical.info', 'pest_id',
                                      string="Technical % Info")
    note = fields.Html(string="Notes")
    group_user_emails = fields.Char(
        string="Group Emails Display",
        compute="_compute_group_user_emails",
        store=True
    )

    @api.model
    def create(self, vals):
        if vals.get('name') == 'New':
            seq = self.env['ir.sequence'].next_by_code('pesticides.reg.sequence')
            vals['name'] = seq
        return super(PesticidesReg, self).create(vals)

    @api.onchange('product')
    def _onchange_product(self):
        if self.product:
            self.brand = self.product.brand_id.name or ''
            self.generic = self.product.generic_name_id.name or ''

    @api.onchange('reg_date', 'expiry_date')
    def _onchange_state(self):
        for record in self:
            if record.reg_date and record.expiry_date:
                if record.expiry_date <= date.today():
                    record.state = 'expired'
                else:
                    record.state = 'registered'

    @api.depends('expiry_date', 'state')
    def _compute_alert(self):
        for record in self:
            if record.state in ['draft', 'applied', 'renewal', 'declined']:
                record.alert = 'none'
            else:
                today = date.today()
                if record.expiry_date:
                    d1 = record.expiry_date - relativedelta(months=2)
                    d2 = d1 - timedelta(days=10)
                    if d2 <= today < d1:
                        record.alert = 'imp'
                    elif today >= d1:
                        record.alert = 'urgent'
                    else:
                        record.alert = 'none'
                else:
                    record.alert = 'none'

    @api.model
    def _cron_pest_updates(self):
        records = self.search([])
        for record in records:
            if record.reg_date and record.expiry_date:
                if record.state == 'registered':
                    if record.expiry_date <= date.today():
                        record.state = 'expired'

            # Stores actual alert stage and computes new

            prev_alert = record.alert
            record._compute_alert()

            # Compute email groups

            record._compute_group_user_emails()

            # Compares alert stages prev and now

            if record.alert in ['imp', 'urgent']:
                if prev_alert != record.alert:
                    record.action_send_email()

    @api.depends()
    def _compute_group_user_emails(self):
        for record in self:
            group = self.env['res.groups'].search(
                [('name', '=', 'Registration Alerts')], limit=1)
            if group:
                user_emails = group.users.mapped('email')
                record.group_user_emails = ', '.join(filter(None, user_emails))
            else:
                record.group_user_emails = ''

    def action_send_email(self):
        template_id = self.env.ref('snc_product_registration.email_pesticides')
        if template_id:
            template_id.send_mail(self.id, force_send=True)
