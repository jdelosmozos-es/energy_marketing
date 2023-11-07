from odoo import models, fields

class EnergyRate(models.Model):
    _name = 'energy.rate'
    _description = 'Energy rate'
    
    name = fields.Char(required=True) #tracking??
    description = fields.Text()
    
    #Secuencia para ordenar?