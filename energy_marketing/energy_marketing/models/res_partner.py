from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    trading_company = fields.Many2one(comodel_name='energy.trading.partner',compute='_compute_trading_company')
    
    @api.depends('name')
    def _compute_trading_company(self):
        for record in self:
            search = self.env['energy.trading.partner'].search([('partner','=',record.id)])
            if search:
                record.trading_company = search[0]
            else:
                record.trading_company = False

    
    def action_create_trading_company(self):
        self.ensure_one()
        res = self.env['energy.trading.partner'].create({'partner': self.id,})
        return
#        return {
#                'name':_('Energy trading company'),
#                'view_mode': 'form',
#                'res_model': 'energy.trading.partner',
#                'res_id': res.id,
#                'type': 'ir.actions.act_window',
#                'nodestroy': True,
#                'target': 'current',
#                'domain': '[]',
#            }