from odoo import fields, models


class CostHide(models.Model):
    _inherit = 'product.template'




class HideCost(models.Model):
    _inherit = 'product.product'

    company_currency_id = fields.Many2one(
        'res.currency', 'Valuation Currency', compute='_compute_value_svl', compute_sudo=True,
        help="Technical field to correctly show the currently selected company's currency that corresponds "
             "to the totaled value of the product's valuation layers")
    avg_cost = fields.Monetary(string="Average Cost", compute='_compute_value_svl', compute_sudo=True,
                               currency_field='company_currency_id', groups="snc_hide_cost.groups_view_standard_price")
    total_value = fields.Monetary(string="Total Value", compute='_compute_value_svl', compute_sudo=True,
                                  currency_field='company_currency_id',
                                  groups="snc_hide_cost.groups_view_standard_price")
