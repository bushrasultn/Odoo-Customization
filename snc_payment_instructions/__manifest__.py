
{
    'name': "Payment Instructions",

    'summary': "Payment Instructions ",
    'sequence': '-100',

    'author': "SunCrop",
    'version': '0.1',
    'application': 'True',
    'depends': ['base', 'mail','snc_custom_report', 'account','snc_payment_customization','contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/record_rules.xml',
        'views/paymnt_instrctn.xml',
        'views/prtner_inhert.xml',
        'views/configuration.xml',
        'views/custom_accounts_views.xml',
        'reports/instruction_header.xml',
        'reports/report_action.xml',
        'reports/report_templte.xml',


    ],
    'installable': True,
    'application': True,

}
