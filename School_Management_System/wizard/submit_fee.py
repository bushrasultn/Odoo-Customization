from odoo import models, fields


class SubmitFeeWizard(models.TransientModel):
    _name = "submit.fee.wizard"
    _description = "Submit Fee Wizard"

    partners_id = fields.Many2one('school.partners', string="Students")
    class_id = fields.Many2one('school.class', string="Class")
    session_id = fields.Many2one('school.session', string="Session")
    fee = fields.Float(string='Submit By')
    date = fields.Date(string='Due Date')

    def _default_student_ids(self):
        return self.env['student.fee'].search([]).ids

    def action_print_report(self):
        student_fees = self.env['student.fee'].search([])
        # student_fees = self.env['student.fee'].search([('partner_id', '=', 'partners_id.id')])
        # student_fees = self.env['student.fee'].browse(ids)
        # brwose method mn pk value ki base pr data search krty hnn
        # student_fees = self.env['student.fee'].search([('class_id', '=', self.class_id.id)])
        # student_fees = self.env['student.fee'].search([('session_id', '=', self.session_id.id)])
        # search method main exact field ka name self . ka mtlb oski property class id fr  list jsko oper defined krty hnn
        student_fee_data = []
        for fee in student_fees:
            for record in fee.student_line_ids:
                student_fee_data.append({
                    'student_name': record.student_id.name,
                    'class': fee.class_id.name,
                    'session': fee.session_id.year,
                    'fee': fee.fee,
                    'date': fee.date
                })

        data = {
            'form': self.read()[0],
            'student_fee_data': student_fee_data
        }
        return self.env.ref('School_Management_System.action_report_student_fee').report_action(self, data=data)
    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
