from odoo import models, fields

class EnergyContractRenewingPeriod(models.Model):
    _name = 'energy.contract.renewing.period'
    _description = 'Period in months to use in contract renewing'
    
    name = fields.Char(required=True, translate=True)
    period_in_months = fields.Integer(required=True,help='Number of months to renew')