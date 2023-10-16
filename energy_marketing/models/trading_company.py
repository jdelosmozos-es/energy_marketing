from odoo import models, fields

class TradingCompany(models.Model):
    _name = 'energy.trading.partner'
    _description = 'Extension of partner for energy trading company'
    _inherits = {'res.partner': 'partner'}
    _inherit = ['mail.thread','mail.activity.mixin']
    
    partner = fields.Many2one(comodel_name='res.partner', required=True, readonly=True, ondelete='restrict', domain="[('is_company','=',True)]")
#    contracts
    contract_types = fields.One2many(comodel_name='energy.trading.contract.type', inverse_name='trading_partner')
    
    
class TradingContractType(models.Model):
    _name = 'energy.trading.contract.type'
    _description = 'Type of contract a trading company sells'
    
    name = fields.Char(required=True)
    trading_partner = fields.Many2one(comodel_name='energy.trading.partner', required=True)
    description = fields.Html()