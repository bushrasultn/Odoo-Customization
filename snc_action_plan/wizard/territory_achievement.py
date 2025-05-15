import json
from odoo import api, fields, models
from datetime import datetime


class TerritoryWizard(models.TransientModel):
    _name = 'territory.wizard'
    _description = 'Territory Wizard'

    date_from = fields.Date(
        string='Date From',
        default=datetime(datetime.now().year, 1, 1)
    )
    date_to = fields.Date(
        string='Date To',
        default=datetime.now().date()
    )
    region = fields.Many2one('customer.region', string='Region')
    territory_id = fields.Many2many('customer.territory', string='Territory', domain="[('region_id', '=', region)]")

    @api.onchange('region')
    def _onchange_region(self):
        if self.region:
            territories = self.env['customer.territory'].search([('region_id', '=', self.region.id)])
            self.territory_id = territories
        else:
            self.territory_id = False

    company_id = fields.Many2one(
        'res.company',
        string='Current Company',
        required=True,
        readonly=True,
        default=lambda self: self.env.context.get('company_id', self.env.company.id)
    )

    def view_report(self):

        data = {
            'company_id': self.company_id.id,
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'territory_ids': self.territory_id.ids,
            'region_name': self.region.name,
            'report_type': 'html'
        }

        data_json = json.dumps(data)
        report_action = self.env.ref('snc_action_plan.view_action_territory_achievement')
        report_url = f"/report/html/{report_action.report_name}?options={data_json}&context={{}}"
        return {
            'type': 'ir.actions.act_url',
            'url': report_url,
            'target': 'new',
        }

    def download_report(self):
        data = {
            'company_id': self.company_id.id,
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'territory_ids': self.territory_id.ids,
            'region_name': self.region.name,
            'report_type': 'pdf'

        }
        download_action = 'snc_action_plan.download_action_territory_achievement'
        return self.env.ref(download_action).report_action(self, data=data)
###########################################################################################################
