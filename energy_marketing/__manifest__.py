{
    'name': 'Energy marketing',
    'version': '15.0.1.0.0',
    'summary': 'Management of company that marketeers energy.',
    'category': 'Sale',
    'author': 'Aarón Misis, Javier L. de los Mozos',
    'maintainer': 'Aarón Misis, Javier L. de los Mozos',
    'depends': ['contacts','partner_multi_relation','web_domain_field','hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/relation_data.xml',
        'views/trading_partner_views.xml',
        'views/res_partner_views.xml',
        'views/energy_rate_views.xml',
        'wizards/contract_incidence_wizard_view.xml',
        'wizards/contract_resolution_wizard_view.xml',
        'views/contract_views.xml',
        'views/renewing_period_views.xml',
        'views/contract_incidence_views.xml',
        'views/menus.xml',
        'data/sequence.xml',
        'views/mail_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
                'energy_marketing/static/src/css/styles.scss',
            ],
    },
    'images': ['static/description/icon.png'],
    'license': 'Other proprietary',
    'installable': True,
    'application': False
}