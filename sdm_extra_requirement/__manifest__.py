{
    'name': "SDM Extra Requirement",
    'category': 'CRM',
    'summary': """Extra Requirement Features for SDM""",
    'author': "Mano Durga/Sidmec",
    'website': "https://sidmectech.com",
    'maintainer': 'Sidmec',
    'description': """Extra Requirement Features for SDM""",
    'version': '18.0.1.0',
    'depends': ['base','mail','project','hr','sale',],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'data/sequence.xml',
        'views/extra_requirement_view.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
