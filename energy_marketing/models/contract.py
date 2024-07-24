from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from random import randint
import json
from dateutil.relativedelta import relativedelta

STATES = [('initial','Created'),
        ('loaded','Uploaded'),
        ('in_progress','In progress'),
        ('liquidated','Liquidated'),
        ('renewed','Renewed'),
        ('incidence','Incidence'),
        ('reversed','Reversed'),
        ('closed','Closed'),
        ('cancelled','Cancelled')
]

class EnergyContract(models.Model):
    _name = 'energy.contract'
    _description = 'Contract of a customer (contact) with an Energy Trading Company.'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    def _not_trading_company_domain(self):
        partners = self.env['res.partner'].search([]) - self.env['energy.trading.partner'].search([]).mapped('partner')
        return [('id','in',partners.ids)]
    
    def get_default_renewing_period(self):
        return self.env.ref('energy_marketing.annual_contract_renewing_period').id

    name = fields.Char(string='Code', readonly=True, required=True, copy=False, default='New')
    salesperson = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user,
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)
    parent_id = fields.Many2one('hr.employee', string='Gerente', related='salesperson.employee_id.parent_id', store=True)   
    partner = fields.Many2one(
        'res.partner', string='Customer', check_company=True, index=True, required=True,
        domain=_not_trading_company_domain,
        )
    state = fields.Selection(selection=STATES,default='initial', tracking=True)
    last_state = fields.Selection(selection=STATES, string='Last state')
    active = fields.Boolean(default=True)
    delegate = fields.Many2one(
            'res.partner', string='Delegate', check_company=True, index=True, tracking=True,
        )
    delegated_domain = fields.Char(compute='_compute_delegated_domain')
    rate = fields.Many2one(comodel_name='energy.rate', tracking=True,states={
                               'loaded':[('required',True)],
                               'incidence':[('required',True)],
                               'in_progress':[('required',True)],
                               'liquidated':[('required',True)],
                               'reversed':[('required',True)],
                               'renewed':[('required',True)],
                               'closed':[('required',True)]})
    trading_company = fields.Many2one(comodel_name='energy.trading.partner', tracking=True,states={
                               'loaded':[('required',True)],
                               'incidence':[('required',True)],
                               'in_progress':[('required',True)],
                               'liquidated':[('required',True)],
                               'reversed':[('required',True)],
                               'renewed':[('required',True)],
                               'closed':[('required',True)]})
    avatar_128 = fields.Binary(related='trading_company.avatar_128')
    contract_type = fields.Many2one(comodel_name='energy.trading.contract.type', tracking=True, domain="[('trading_partner','=',trading_company)]",states={
                               'loaded':[('required',True)],
                               'incidence':[('required',True)],
                               'in_progress':[('required',True)],
                               'liquidated':[('required',True)],
                               'reversed':[('required',True)],
                               'renewed':[('required',True)],
                               'closed':[('required',True)]})
    # commission = Many2one(comodel_name='energy.marketing.commission') DEBERÍA SER TIPO DE COMISIÓN???
    # Yo creo que debe haber una línea por cada comisión con fecha, importe y estado que dependerá de si está facturada o no.
    # Hay que ver en qué estado deben ser required qué campos.
    company_id = fields.Many2one(
        'res.company', string='Company', index=True)
    user_company_ids = fields.Many2many(
        'res.company', compute='_compute_user_company_ids',
        help='UX: Limit to lead company or all if no company')
    #receipts = fields.One2many(comodel_name='energy.contract.recepit', inverse_name='contract')
    date = fields.Date(states={
                               'loaded':[('required',True)],
                               'incidence':[('required',True)],
                               'in_progress':[('required',True)],
                               'liquidated':[('required',True)],
                               'reversed':[('required',True)],
                               'renewed':[('required',True)],
                               'closed':[('required',True)]})
    end_date = fields.Date(compute="_compute_end_date", store=True)
    renewing_period = fields.Many2one(comodel_name='energy.contract.renewing.period',default=get_default_renewing_period, required=True)
    CUPS = fields.Char(string='CUPS',states={
                               'loaded':[('required',True)],
                               'incidence':[('required',True)],
                               'in_progress':[('required',True)],
                               'liquidated':[('required',True)],
                               'reversed':[('required',True)],
                               'renewed':[('required',True)],
                               'closed':[('required',True)]})
    balance = fields.Monetary(compute='_compute_balance')
    currency_id = fields.Many2one('res.currency', compute='_compute_currency', string="Currency")
    vat = fields.Char(related='partner.vat',search='_search_vat')
    incidence_ids = fields.One2many(comodel_name='energy.contract.incidence', inverse_name='contract')
    incidence_count = fields.Integer(compute='_compute_incidence_count')
    category_ids = fields.Many2one(
        'energy.contract.category',
        string='Tipo')
    delay = fields.Integer(string='Delay', default=24)
    management_tasks = fields.Many2many(comodel_name='energy.contract.management.task')

    @api.depends('date','renewing_period')
    def _compute_end_date(self):
        for record in self:
            if record.date:
                self.end_date = record.date + relativedelta(months=record.renewing_period.period_in_months)
            else:
                self.end_date = False

    def _compute_incidence_count(self):
        for record in self:
            incidences = self.env['energy.contract.incidence'].search([('contract','=',record.id)])
            record.incidence_count = len(incidences)

    def _search_vat(self, operator, value):
        allowed_partners = self.env["res.partner"].sudo().search([("", operator, value)])
        return [("partner", "in", allowed_partners.ids)]
        
    @api.depends('company_id')
    def _compute_currency(self):
        for record in self:
            record.currency_id = record.company_id.currency_id
    
#    @api.depends('receipts','')
    
    @api.constrains('CUPS')
    def _CUPS_constraint(self):
        all_records = self.search([])
        for record in self:
            if record.CUPS:
                if record.CUPS in (all_records - record).mapped('CUPS'):
                    raise ValidationError('CUPS %s already exists.' % record.CUPS)
        
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
                ('left_partner_id','=',self.partner.id)
                ]).mapped('right_partner_id')
        self.delegated_domain = json.dumps([('id','in',partners.ids)])
        
    @api.model   
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('contract') or 'New'
        result = super(EnergyContract, self).create(vals) 
        return result
    
    def generate_message(self):
        channel_id = self.env.ref('energy_marketing.channel_administration_departament', raise_if_not_found=False)  
        if channel_id:
            contract_url = ("<b><a href='#id=%s&model=%s'>%s</a></b>") % (self.id, self._name,self.name)
            if self.state == 'initial':
                message = '' + contract_url + (" - El contrato ha sido creado por:  <b>%s</b>") % self.salesperson.name
            else:
                message = '' + contract_url + (" - El contrato ha pasado al estado:  <b>%s</b>") % (dict(self._fields.get('state').selection).get(self.state))                
            channel_id.message_post(
                body=(message),
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def next_state(self):      
        for record in self:
            if record.state == 'initial':
                record.state = 'loaded'
            elif record.state == 'loaded':
                record.state = 'in_progress'
            elif record.state == 'renewed':
                record.state = 'in_progress'
            record.generate_message()

    @api.model
    def generate_incidence(self):
        for record in self:
            record.last_state = record.state
            record.state = 'incidence'
            record.generate_message()
            
    def resolve_incidence(self):
        for record in self:
            if record.state == 'incidence':
                record.state = record.last_state
                record.generate_message()

    def generate_liquidation(self):
        for record in self:
            record.state = 'liquidated'
            record.generate_message()

    def reverse_contract(self):
        for record in self:
            record.state = 'reversed'
            record.generate_message()

    def renewed_contract(self):
        for record in self:
            record.state = 'renewed'
            record.generate_message()

    def cancel_contract(self):
        for record in self:
            for incidence in record.incidence_ids:
                if incidence.state == 'open':
                    incidence.state = 'no_resolution'
            record.state = 'cancelled'
            record.generate_message()

    def contract_incidences(self):
        action = self.env["ir.actions.actions"]._for_xml_id("energy_marketing.energy_action_contract_incidences")
        action['domain'] = [('contract','=',self.id)]
        return action
    
    def create_activity(self, user, message):
        activity_type =  self.env.ref('mail.mail_activity_data_todo')
        self.env['mail.activity'].sudo().create({
            'activity_type_id': activity_type.id,
            'date_deadline': fields.Date.context_today(self),
            'res_id': self.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model','=', 'energy.contract')]).id,
            'user_id': user.id,
            'summary': message,
        })
        
    def get_administration_user_ids(self):
        return self.env['res.users'].search([('groups_id','in',self.env.ref('base.group_user').id)]).ids
    
    def _find_mail_template(self, force_confirmation_template=False):
        template_id = self.env.ref('energy_marketing.email_template_energy_contract', raise_if_not_found=False).id
            
        return template_id
    
    def kanban_send_mail(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'energy.contract',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'model_description': self.with_context(lang=lang).CUPS,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


class ContractCategory(models.Model):

    _name = "energy.contract.category"
    _description = "Contract Category"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)
    employee_ids = fields.Many2many('energy.contract', 'energy_contract_category_rel', 'category_id', 'contract_id', string='Contracts')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    