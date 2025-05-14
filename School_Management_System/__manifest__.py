{
    'name': "School Management System",
    'summary': "School ",
    'sequence': '-100',
    'author': "Bushra",
    'version': '0.1',
    'application': True,
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'wizard/teacher_admin.xml',
        'wizard/submit_fee.xml',
        'views/partners.xml',
        'views/subject.xml',
        'views/class.xml',
        "data/sequence.xml",
        'views/session.xml',
        'views/console.xml',
        'views/result.xml',
        'views/fee.xml',
'views/parent_menu.xml',
        'reports/student_report.xml',
        'reports/report.xml',
        'reports/submit_template.xml',
        'reports/submit.xml'
    ],
    'installable': True,
    # 'auto_install': False,
}
