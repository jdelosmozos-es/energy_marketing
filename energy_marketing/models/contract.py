from odoo import models, fields, api
import json

class EnergyContract(models.Model):
    _name = 'energy.contract'
    _description = 'Contract of a customer (contact) with an Energy Trading Company.'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    def _not_trading_company_domain(self):
        partners = self.env['res.partner'].search([]) - self.env['energy.trading.partner'].search([]).mapped('partner')
        return [('id','in',partners.ids)]    
    
    name = fields.Char(string='Code')    
    salesperson = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user,
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)
    partner = fields.Many2one(
        'res.partner', string='Customer', check_company=True, index=True, required=True,
        domain=_not_trading_company_domain,
        )
    state = fields.Selection(selection=[
            ('initial','Initial'),
            ('in_progress','In progress'),
            ('settled','Settled'),
            ('reversed','Reversed'),
            ('renewed','Renewed'),
            ('closed','Closed')
        ],default='initial')
    active = fields.Boolean(default=True)
    delegate = fields.Many2one(
            'res.partner', string='Delegate', check_company=True, index=True, tracking=True,
        )
    delegated_domain = fields.Char(compute='_compute_delegated_domain')
    rate = fields.Many2one(comodel_name='energy.rate', tracking=True,)
    trading_company = fields.Many2one(comodel_name='energy.trading.partner', tracking=True)
    contract_type = fields.Many2one(comodel_name='energy.trading.contract.type', tracking=True, domain="[('trading_partner','=',trading_company)]")
    # commission = Many2one(comodel_name='energy.marketing.commission') DEBERÍA SER TIPO DE COMISIÓN???
    # Yo creo que debe haber una línea por cada comisión con fecha, importe y estado que dependerá de si está facturada o no.
    # Hay que ver en qué estado deben ser required qué campos.
    company_id = fields.Many2one(
        'res.company', string='Company', index=True)
    user_company_ids = fields.Many2many(
        'res.company', compute='_compute_user_company_ids',
        help='UX: Limit to lead company or all if no company')
    
    @api.depends('company_id')
    def _compute_user_company_ids(self):
        all_companies = self.env['res.company'].search([])
        for contract in self:
            if not contract.company_id:
                contract.user_company_ids = all_companies
            else:
                contract.user_company_ids = contract.company_id
                
    @api.depends('partner')
    def _compute_delegated_domain(self):
        self.ensure_one()
        relation = self.env.ref('energy_marketing.delegate_relation')
        partners = self.env['res.partner.relation'].search([
                ('type_id','=',relation.id),
                ('right_partner_id','=',self.partner.id)
                ]).mapped('left_partner_id')
        self.delegated_domain = json.dumps([('id','in',partners.ids)])
