# -*- coding: utf-8 -*-
{
    'name': "ACT | Product Costimator",

    'summary': "Real-time BOM cost calculator for manufacturing using current market prices.",

    'description': """
ACT Product Costimator
Ideal for manufacturing companies that need real-time and accurate production costing.
    """,

    'author': "Actination",

    'depends': ['base', 'product', 'mrp'],

    'data': [
        'security/ir.model.access.csv',
        'views/parent_menu.xml',
        'views/product_costimator.xml',
        'views/configuration.xml',
    ],
}