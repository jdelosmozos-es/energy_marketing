from odoo import models, fields

class ContractReceipt(models.Model):
    _name = 'energy.contract.receipt'
        
    contract = fields.Many2one(comodel_name='energy.contract')
    periodo una secuencia empezando en cero para cada contrato o mes/año empezando en la fecha de firma
    amount = fields.Monetary
    cobrado boolean
    payments = fields.One2many(comodel_name='ebergy.contract.payment', inverse_name='receipt')
    total pagado: compute
    falta por pagar: compute
    
    #constraint la suma de payments.mapped('amount') no puede ser mayor que self.amount