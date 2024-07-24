from odoo import models, fields

class ContractManagementTask(models.Model):
    _name = 'energy.contract.management.task'
    _description = 'Model for any management task that could be done on a contract.'
    
    main_contract = fields.Many2one(comodel_name='energy.contract')
    
class ContractManangementPowerChangeTask(models.Model):
    _name = 'energy.contract.management.power.change.task'
    _inherit = 'energy.contract.management.task'
    _description = 'Change of power in a contract.'
    
    previous_power = fields.Float()
    new_power = fields.Float()