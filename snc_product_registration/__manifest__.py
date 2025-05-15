{
    'name': "Product Registration",
    'summary': "Product registration module",
    'sequence': '-100',
    'author': "SunCrop",
    'version': '0.1',
    'application': True,
    'depends': ['base', 'mail', 'product'],

    # Always loaded data
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/config.xml',
        'views/ipo.xml',
        'views/pesticides.xml',
        'views/fertilizer.xml',
        'reports/pesticides_form.xml',
        'reports/report_action.xml',
        'reports/report_header.xml',
    ],
    'installable': True,
    'application': True,
}
