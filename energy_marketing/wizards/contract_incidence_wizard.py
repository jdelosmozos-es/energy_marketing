from odoo import models, fields, api

class ContranctIncidenceWizard(models.TransientModel):
    _name = 'contract.incidence.wizard'
    _description = 'Wizard to create incidences for contracts.'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)
    contract = fields.Many2one(comodel_name='energy.contract', string='Contract', required=True)

    def generate_incidence(self):
        self.env['energy.contract.incidence'].create({
            'name': self.name,
            'description': self.description,
            'contract': self.contract.id,
            'contract_state': self.contract.state,
        })
        self.contract.generate_incidence()
        return {'type': 'ir.actions.act_window_close'}