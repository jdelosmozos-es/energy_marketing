from odoo import models, fields, api

class EnergyContract(models.Model):
    _name = 'energy.contract'
    _description = 'Contract of a customer (contact) with an Energy Trading Company.'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    def _delegated_domain(self):
        relation = self.env['res.partner.relation.type'].browse(self.env.ref('res.partner.relation.type'))
        partners = self.env['res.partner.relation.all'].search([
            ('type_selection_id','=',relation.id),
            ('other_partner_id','=',self.partner.id)
            ])
        return [('id','in',partners.ids),'|', ('company_id', '=', False), ('company_id', '=', self.company_id)]
        
        
    salesperson = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user,
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)
    partner = fields.Many2one(
        'res.partner', string='Customer', check_company=True, index=True, required=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        )
    state = fields.Selection(selection=[
            ('initial','Initial'),
            ('in_progress','In progress'),
            ('settled','Settled'),
            ('reversed','Reversed'),
            ('renewed','Renewed'),
            ('closed','Closed')
        ],)
    active = fields.Boolean()
    delegate = fields.Many2one(
        'res.partner', string='Delegate', check_company=True, index=True, tracking=True,
        domain=_delegated_domain,
        ) #FIXME: el domain debe obligar a que sea un representante.
    rate = fields.Many2one(comodel_name='energy.rate', tracking=True,)
    trading_company = fields.Many2one(comodel_name='energy.trading.partner', tracking=True)
    contract_type = fields.Many2one(comodel_name='energy.trading.contract.type', tracking=True, domain="[('trading.partner','=',trading_company.id)]")
    # commission = Many2one(comodel_name='energy.marketing.commission') DEBERÍA SER TIPO DE COMISIÓN???
    # Yo croe que debe haber una línea por cada comisión con fecha, importe y estado que dependerá de si está facturada o no.
    # Hay que ver en qué estado deben ser required qué campos.
    company_id = fields.Many2one(
        'res.company', string='Company', index=True)
    