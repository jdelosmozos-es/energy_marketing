from odoo import models, fields, api

class ContranctResolutionWizard(models.TransientModel):
    _name = 'contract.resolution.wizard'
    _description = 'Wizard to create resolutions for incidences.'

    description = fields.Char(string='Resolution', required=True)
    contract = fields.Many2one(comodel_name='energy.contract', string='Contract', required=True)

    def generate_resolution(self):
        incidence = self.env['energy.contract.incidence'].search([('contract','=',self.contract.id),('state','=','open')],limit=1)
        incidence.resolution = self.description
        incidence.state = 'closed'
        self.contract.resolve_incidence()
        return {'type': 'ir.actions.act_window_close'}