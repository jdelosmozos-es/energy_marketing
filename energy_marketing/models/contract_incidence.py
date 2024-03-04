from odoo import models, fields

CONTRACT_STATES = [('initial','Created'),
        ('loaded','Uploaded'),
        ('incidence','Incidence'),
        ('in_progress','In progress'),
        ('liquidated','Liquidated'),
        ('reversed','Reversed'),
        ('renewed','Renewed'),
        ('closed','Closed'),
        ('cancelled','Cancelled')
]

class ContractIncidence(models.Model):
    _name = 'energy.contract.incidence'
    _description = 'Incidence for a contract.'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)
    resolution = fields.Char(string='Resolution', required=True)
    contract = fields.Many2one(comodel_name='energy.contract', required=True, string='Contract')
    state = fields.Selection(selection=[('open','Open'),('no_resolution','No Resolution'),('closed','Closed')], default='open', string='State', tracking=True)
    contract_state = fields.Selection(selection=CONTRACT_STATES, string='Contract state')
    partner = fields.Many2one(related="contract.partner", string='Customer', store=True)
    salesperson = fields.Many2one(related="contract.salesperson", string='Salesperson', store=True)
