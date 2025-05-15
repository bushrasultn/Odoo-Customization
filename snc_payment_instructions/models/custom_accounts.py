from odoo import api, fields, models


class CustomAccounts(models.Model):
    _name = 'custom.accounts'
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
