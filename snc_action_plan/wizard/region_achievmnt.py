from odoo import models, fields, api
from datetime import datetime
import json

class RegionAchievementWizard(models.TransientModel):
    _name = 'region.achievement.wizard'
    _description = 'Achievement Wizard'

    date_from = fields.Date(
        string='Date From',
        default=datetime(datetime.now().year, 1, 1)
    )

    date_to = fields.Date(
        string='Date To',
        default=datetime.now().date()
    )

    company_id = fields.Many2one(
        'res.company',
        string='Current Company',
        required=True,
        readonly=True,
        default=lambda self: self.env.context.get('company_id', self.env.company.id)
    )
    region_id = fields.Many2many('customer.region', string='Region')

    def view_report(self):
        data = {
            'company_id': self.company_id.id,
            'region_ids': self.region_id.ids,
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'report_type': 'html'
        }
        data_json = json.dumps(data)

        report_action = self.env.ref('snc_action_plan.view_action_region_achievement')
        report_url = f"/report/html/{report_action.report_name}?options={data_json}&context={{}}"

        return {
            'type': 'ir.actions.act_url',
            'url': report_url,
            'target': 'new',
        }

    def download_report(self):
        data = {
            'company_id': self.company_id.id,
            'region_ids': self.region_id.ids,
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'report_type': 'pdf'
        }
        download_action = 'snc_action_plan.download_action_region_achievement'
        return self.env.ref(download_action).report_action(self, data=data)


