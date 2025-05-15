from odoo import models, fields


class CustomLocation(models.Model):
    _name = 'return.location'
    _description = 'Returnable Location'

    name = fields.Char(string='Location Name')
    type = fields.Selection(
        [('wh transfer', 'WH Transfer'), ('vendor', 'Vendor')],
        string='Type'
    )
    warehouse = fields.Many2one('stock.warehouse', string='Warehouse')
    is_transit = fields.Boolean(string='Is Transit Location')
