from odoo import models
from odoo import fields


class InheritSaleTeam(models.Model):
    _inherit = 'crm.team'
    _description = 'Crm Team'

    stages = fields.Many2one('crm.stage')


class InheritSales(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super(InheritSales, self).action_confirm()
        self.team_id.stages = self.opportunity_id.stage_id