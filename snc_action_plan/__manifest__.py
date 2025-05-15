{
    'name': "National Action Plan",

    'summary': "Action Plan & Achievements",
    'sequence': '-100',

    'author': "Sun Crop",
    'version': '0.1',
    'application': 'True',
    'depends': ['base', 'mail', 'event', 'hr_expense'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/record_rules.xml',
        'wizard/territory_achievement.xml',
        'wizard/region_achievmnt.xml',
        "views/target.xml",
        "views/view.xml",
        "views/menu.xml",
        "views/checklist.xml",
        "reports/report_action.xml",
        "reports/custom_header.xml",
        "reports/region_achievement.xml",
        "reports/territory_achievement.xml",
    ],

}
