from odoo import api, models


class WHStockReport(models.AbstractModel):
    _name = 'report.School_Management_System.student_fee'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        data = data or {}

        class_id = data.get('class_id')
        session_id = data.get('session_id')
        date = data.get('date')
        student_ids = data.get('student_ids', [])
        records = self.env['school.student'].search([('id', 'in', student_ids)])
        fee = self._get_fee_info(student_ids)
        return {
            'class_id': class_id,
            'session_id': session_id,
            'fee': fee,
            'date': date,
            'students': records
        }
    def _get_fee_info(self, student_ids):
        return {}
