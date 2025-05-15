from odoo import models, fields, api


class Undertaking(models.Model):
    _name = 'name.undertaking'
    _description = 'Name Undertaking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name Undertaking", Tracking=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################
class Category(models.Model):
    _name = 'category.name'
    _description = 'Category Name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Category Name")
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env.user.company_id.id
    )

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################

class FormType(models.Model):
    _name = 'form.type'
    _description = 'Form Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )
    name = fields.Char(string="Name", Tracking=True)

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################

class OriginCountry(models.Model):
    _name = 'origin.reg'
    _description = 'Origin Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )
    name = fields.Char(string="Name", Tracking=True)

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################


class ProvinceReg(models.Model):
    _name = 'province.reg'
    _description = 'Registration Province'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )
    name = fields.Char(string="Name", Tracking=True)

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################

class RegistrationDepartment(models.Model):
    _name = 'depart.reg'
    _description = 'Registration Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )
    name = fields.Char(string="Name", Tracking=True)

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################

class Formulation(models.Model):
    _name = 'form.reg'
    _description = 'Formulation Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )
    name = fields.Char(string="Name", Tracking=True)

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################


class StagesIPO(models.Model):
    _name = 'stage.ipo'
    _description = 'Stages IPO'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )
    name = fields.Char(string="Name", Tracking=True)

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################
class fertilizerdepartment(models.Model):
    _name = "fertilizer.dept"
    _description = "fertilizer department"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True, required=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda rec: rec.env.user.company_id.id
    )

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res


###############################################################################

class fertilizerUndertaking(models.Model):
    _name = "fertilizer.undertaking"
    _description = "Fertilizer Name Undertaking"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True, required=True)
    company_id = fields.Many2one(
    comodel_name='res.company',
    default=lambda rec: rec.env.user.company_id.id
)

    @api.model
    def create(self, vals_list):
        vals_list['company_id'] = self.env.context['allowed_company_ids'][0]
        res = super().create(vals_list)
        return res
