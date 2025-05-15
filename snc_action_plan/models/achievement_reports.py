from odoo import models, fields, api
from datetime import datetime
import json


######################################################################
##                                                                  ##
##                   Monthly Region_Achievement Report             ##
##                                                                  ##
######################################################################
class RegionAchievementReport(models.AbstractModel):
    _name = 'report.snc_action_plan.region_achievement_id'

    def _get_report_values(self, docids=None, data=None):
        company_id = data.get('company_id')
        company = self.env['res.company'].browse(company_id)
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        rep_type = data.get('report_type')
        achievement = self.env['event.event'].search([
            ('region_id', 'in', data.get('region_ids')),
            ('date_begin', '>=', date_from),
            ('date_end', '<=', date_to),
            ('verify', '=', True)
        ])
        event_type = achievement.mapped('event_type_id')

        return {
            'company_name': company.name,
            'company_street': company.partner_id.street,
            'rep_type': rep_type,
            'date_from': date_from,
            'date_to': date_to,
            'achievement': achievement,
            'event_type': event_type,
            'regions': self.env['customer.region'].browse(data.get('region_ids')),
        }


######################################################################
##                                                                  ##
##                    Monthly Territory_Achievement Report         ##
##                                                                  ##
######################################################################
class TerritoryAchivementReport(models.AbstractModel):
    _name = 'report.snc_action_plan.report_territory_achievement'

    def _get_report_values(self, docids=None, data=None):
        company_id = data.get('company_id')
        company = self.env['res.company'].browse(company_id)
        date_from = datetime.strptime(data.get('date_from'), '%d-%m-%Y')
        date_to = datetime.strptime(data.get('date_to'), '%d-%m-%Y')
        rep_type = data.get('report_type')
        achievement = self.env['event.event'].search([('territory_id', 'in', data.get('territory_ids'))])
        achievement = achievement.filtered(
            lambda rec: str(rec.date_begin.date()) >= data.get('date_from') and str(rec.date_end.date()) <= data.get(
                'date_to'))
        achievement = achievement.filtered(lambda rec: rec.verify == True)
        region_name = data.get('region_name')
        event_type = achievement.mapped('event_type_id')
        return {
            'company_name': company.name,
            'company_street': company.partner_id.street,
            'rep_type': rep_type,
            'date_from': date_from.strftime('%d-%m-%Y'),
            'date_to': date_to.strftime('%d-%m-%Y'),
            'achievement': achievement,
            'event_type': event_type,
            'territory': self.env['customer.territory'].browse(data.get('territory_ids')),
            'region_name': region_name,
        }


######################################################################
##                                                                  ##
##                    Annual_Achievement Report         ##
##                                                                  ##
######################################################################

