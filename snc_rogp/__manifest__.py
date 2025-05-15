{
    'name': "SNC ROGP",

    'summary': "SNC ROGP",

    'version': '0.1',
    'application': 'True',
    'depends': ['base', 'product', 'stock', 'snc_transport_managment', 'account', ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security_rule.xml',
        'views/rogp.xml',
        'views/rigp.xml',
        'views/custom_location.xml',
        'views/returnables_view.xml',
        # 'views/inward_valuation.xml',
        'report/report_action.xml',
        'report/outward_template.xml',
        'report/inward_template.xml',
        'report/header.xml',
        'data/sequence.xml',

    ],
    'installable': True,
    'application': True,

}
