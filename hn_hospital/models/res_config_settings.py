from odoo import fields, models


class InheritResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(string='Cancel Days',config_parameter ='hn_hospital.cancel_days')
