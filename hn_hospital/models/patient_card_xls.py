# -*- coding: utf-8 -*-

import base64
import io
from odoo import models


class PatientCardXlsx(models.AbstractModel):
    _name = 'report.hn_hospital.report_patient_id_card_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        # sheet = workbook.add_worksheet('patient ID Card')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'red'})

        for obj in patients:
            sheet_name = str(obj.name) if isinstance(obj.name, str) else 'Unknown'
            if len(sheet_name) > 31:
                sheet_name = sheet_name[:31]

            sheet = workbook.add_worksheet(sheet_name)
            row = 3
            col = 3
            sheet.set_column('D:E', 15)
            sheet.set_column('E:F', 15)

            row += 1
            sheet.merge_range(row, col, row, col + 1, 'ID Card', format_1)
            row += 1
            if obj.image:
                try:
                    patient_image = io.BytesIO(base64.b64decode(obj.image))
                    sheet.insert_image(row, col, "image.png",
                                       {'image_data': patient_image, 'x_scale': 0.5, 'y_scale': 0.5})
                except Exception as e:
                    sheet.write(row, col, 'Image Error: ' + str(e))
                row += 6

            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, 'Age', bold)
            sheet.write(row, col + 1, obj.age)
            row += 1
            sheet.write(row, col, 'Reference', bold)
            sheet.write(row, col + 1, obj.reference)
            row += 1

