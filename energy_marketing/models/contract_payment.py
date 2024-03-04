from odoo import models, fields

class ContractPayment(models.Model):
    _name = 'energy.contract.payment'
    _description = 'Payments made for a contract.'
    
    receipt=fields.Many2one(comodel_name='energy.contract.receipt')
    salesperson = fields.Many2one(comodel_name='res.partner') #empleado?
    amount = fields.Monetary
    payment_date = fields.Date() #debería ser un related de invoice.date
    invoice = fields.Many2one(comodel_name='account.move')
