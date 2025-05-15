from odoo import models, fields, api
from odoo import models, fields, api


class InwardGatePass(models.Model):
    _inherit = 'gate.pass'
    _description = 'Inward'



class InwardReturnableValuationLines(models.Model):
    _name = 'inward.returnable.valuation.line'
    _description = 'Returnable Valuation Line'