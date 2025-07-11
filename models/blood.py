from odoo import models, fields, api

class StudentReportByBlood(models.TransientModel):
    _inherit = 'library.student.wizard'
    _description = 'Student Report by Blood Group'

    # পূর্বের shift/class/section ফিল্ড আর দরকার নেই, তাই False সেট করা হলো
    shift_id = False
    class_id = False
    section_id = False

    # নতুন ফিল্ড: রক্তের গ্রুপ
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], string='Blood Group', required=True)

    @api.depends('blood_group')
    def _compute_students(self):
        for wiz in self:
            if wiz.blood_group:
                students = self.env['school.student'].search([
                    ('blood_group', '=', wiz.blood_group),
                ])
                wiz.students_ids = students
            else:
                wiz.students_ids = False

    def action_print_pdf(self):
        # XML-এ 'students.action_report_student_by_blood' নামে report action ডিফাইন করুন
        return self.env.ref('students.action_report_student_by_blood').report_action(self)
