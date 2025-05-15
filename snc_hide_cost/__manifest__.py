{
    'name': "SNC Cost",

    'summary': "SNC Cost",

    'version': '0.1',
    'application': 'True',
    'depends': ['base','product', 'stock','account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/cost.xml',

    ],
    'installable': True,
    'application': True,

}
