from datetime import datetime
from odoo import fields, models, api


class Territorylines(models.Model):
    _name = 'valuation.target'
    _description = 'NAP Territory lines'

    nap_target_id = fields.Many2one('nap.target', string="Nap Target")
    territory = fields.Many2one('customer.territory', string="Territory")
    event_target = fields.Integer(string='Event Target')
    event_type = fields.Many2one('event.type', string='Event Type')


class Target(models.Model):
    _name = 'nap.target'
    _description = 'NAP Targets'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Table Fields

    year = fields.Char(string='Year', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    # mng_level = fields.Selection([('TM', 'TM'), ('RSM', 'RSM')], string='Team Level')
    company = fields.Many2one('res.company', string='Company',
                              default=lambda self: self.env.company,
                              required=True)
    region_ids = fields.Many2many('customer.region', string='Region', required=True)
    event_type = fields.Many2one('event.type', string='Event Type', required=True)
    event_target = fields.Integer(string='Event Target', required=True)
    comments = fields.Html(string='Comments')
    territory = fields.Many2many('customer.territory', string='Territory', required=True,
                                 domain="[('region_id', 'in', region_ids)]")
    terr_lines = fields.One2many('valuation.target', 'nap_target_id', string="Product Lines")

    @api.onchange('year')
    def _onchange_year(self):
        for record in self:
            if record.year:
                record.start_date = datetime(int(record.year), 1, 1).date()
                record.end_date = datetime(int(record.year), 12, 31).date()

    @api.onchange('region_ids')
    def _onchange_region_ids(self):
        if self.region_ids:
            region_ids = self.region_ids.ids
            territories = self.env['customer.territory'].search([('region_id', 'in', region_ids)])
            self.territory = territories
        else:
            self.territory = False

    def action_add_lines(self):
        for record in self:
            lines = []
            for territory in record.territory:
                lines.append((0, 0, {
                    'territory': territory.id,
                    'event_type': record.event_type.id,
                    'event_target': record.event_target,
                }))

            record.terr_lines = None
            record.terr_lines = lines



