{
    'name': 'Energy marketing',
    'version': '15.0.1.0.0',
    'summary': 'Management of company that marketeers energy.',
    'category': 'Sale',
    'author': 'Aarón Misis, Javier L. de los Mozos',
    'maintainer': 'Aarón Misis, Javier L. de los Mozos',
    'depends': ['contacts','partner_multi_relation','web_domain_field'],
    'data': [
        'views/trading_partner_views.xml',
        'views/res_partner_views.xml',
        'views/energy_rate_views.xml',
        'views/contract_views.xml',
        'views/menus.xml',
        'data/relation_data.xml',
        'security/ir.model.access.csv',
#        'security/security.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'Other proprietary',
    'installable': True,
    'application': True
}