from odoo.tools import date_utils
from odoo import models
from odoo import fields
from odoo import api


class InheritCrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_crm_lead(self):
        my_lead = self.env['crm.lead'].search_count([('type', '=', 'lead')])
        lost = self.env['crm.lead'].search_count([('active', '=', False)])
        win = self.env['crm.lead'].search_count([('active', '=', True)])
        opportunity = self.env['crm.lead'].search_count([(
            'type', '=', 'opportunity')])
        expected_revenue = sum(self.env['crm.lead']
                               .search([]).mapped('expected_revenue'))
        revenue = sum(self.env['account.move'].search(
            [('move_type', '=', 'out_invoice')]).mapped('amount_total_signed'))
        win_ratio = win / lost

        return {
            'lead': my_lead,
            'opportunity': opportunity,
            'revenue': revenue,
            'expected_revenue': expected_revenue,
            'win_ratio': win_ratio
        }

    @api.model
    def get_stage_graph(self):
        stages = self.env['crm.stage'].search([]).mapped('name')
        total_count = []
        for i in stages:
            count = self.search_count([('stage_id', '=', i)])
            total_count.append(int(count))
            stage = [stages, total_count]
        return stage

    @api.model
    def get_stage_graph_year(self):
        stages = self.env['crm.stage'].search([]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year).mapped('name')
        total_count = []
        for i in stages:
            count = self.search_count([('stage_id', '=', i)])
            total_count.append(int(count))
        stage = [stages, total_count]
        return stage

    @api.model
    def get_stage_graph_month(self):
        stages = self.env['crm.stage'].search([]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month).mapped(
            'name')
        total_count = []
        for i in stages:
            count = self.search_count([('stage_id', '=', i)])
            total_count.append(int(count))
        stage = [stages, total_count]
        return stage

    @api.model
    def get_stage_graph_week(self):
        stages = self.env['crm.stage'].search([]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1]).mapped(
            'name')
        total_count = []
        for i in stages:
            count = self.search_count([('stage_id', '=', i)])
            total_count.append(int(count))
        stage = [stages, total_count]
        return stage

    @api.model
    def crm_year(self):
        rec = {}
        lead_count = self.search(
            [('type', '=', 'lead')])
        year_lead_count = len(
            [record.create_date.year for record in lead_count if
             fields.Date.today().year == record.create_date.year])+1

        opportunity_count = self.env["crm.lead"].search(
            [('type', '=', 'opportunity'), ('user_id', '=', self.env.user.id)])
        year_opp_count = len(
            [record.create_date.year for record in opportunity_count if
             fields.Date.today().year == record.create_date.year])

        year_expected_revenue = sum(self.env["crm.lead"].search(
            [('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year).mapped(
            "expected_revenue"))
        year_revenue = round(sum(self.env["sale.order"].search(
            [('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year).mapped(
            "amount_total")),
                             2)
        year_win_count = (self.env["crm.lead"]).search(
            [('stage_id.is_won', '=', True),
             ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.year == fields.Date.today().year)
        year_win_list = len([i.id for i in year_win_count])
        year_win_ratio = round(
            (year_win_list / (year_lead_count + year_opp_count)) * 100, 2)
        rec.update({
            'lead_year': year_lead_count,
            'opportunity_year': year_opp_count,
            'expected_rev_year': year_expected_revenue,
            'year_revenue': year_revenue,
            'year_win_ratio': year_win_ratio,
        })
        return rec

    @api.model
    def crm_month(self):
        rec = {}
        month_lead = self.env["crm.lead"].search(
            [('type', '=', 'lead'), ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_lead_count = len([i.id for i in month_lead])

        month_opportunity = self.env["crm.lead"].search(
            [('type', '=', 'opportunity'),
             ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_opp_count = len([i.id for i in month_opportunity])

        month_expected_revenue = sum(self.env["crm.lead"].search(
            [('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month).mapped(
            "expected_revenue"))
        month_revenue = round(sum(self.env["sale.order"].search(
            [('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month).mapped(
            "amount_total")),
                              2)
        month_win_count = (self.env["crm.lead"]).search(
            [('stage_id.is_won', '=', True),
             ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.month == fields.Date.today().month)
        month_win_list = len([i.id for i in month_win_count])
        month_win_ratio = round(
            (month_win_list / (month_lead_count + month_opp_count)) * 100, 2)
        rec.update({
            "month_lead_count": month_lead_count,
            "month_opp_count": month_opp_count,
            "month_expected_revenue": month_expected_revenue,
            "month_revenue": month_revenue,
            "month_win_ratio": month_win_ratio,

        })
        return rec

    @api.model
    def crm_week(self):
        rec = {}
        week_lead = self.env["crm.lead"].search(
            [('type', '=', 'lead')]).filtered(
            lambda x: x.create_date.isocalendar()[1] == fields.Date.today().isocalendar()[1])
        week_lead_count = len([i.id for i in week_lead])

        week_opportunity = self.env["crm.lead"].search(
            [('type', '=', 'opportunity'),
             ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] ==
                      fields.Date.today().isocalendar()[1])
        week_opp_count = len([i.id for i in week_opportunity])

        week_expected_revenue = sum(self.env["crm.lead"].search(
            [('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] ==
                      fields.Date.today().isocalendar()[1]).mapped(
            "expected_revenue"))
        week_revenue = round(sum(self.env["sale.order"].search(
            [('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] ==
                      fields.Date.today().isocalendar()[1]).mapped(
            "amount_total")),
                             2)
        week_win_count = (self.env["crm.lead"]).search(
            [('stage_id.is_won', '=', True),
             ('user_id', '=', self.env.user.id)]).filtered(
            lambda x: x.create_date.isocalendar()[1] ==
                      fields.Date.today().isocalendar()[1])
        week_win_list = len([i.id for i in week_win_count])
        week_win_ratio = round(
            (week_win_list / (week_lead_count + week_opp_count)) * 100, 2)
        rec.update({
            "week_lead_count": len(week_lead),
            "week_opp_count": week_opp_count,
            "week_expected_revenue": week_expected_revenue,
            "week_revenue": week_revenue,
            "week_win_ratio": week_win_ratio,
        })
        return rec

    @api.model
    def crm_quarter(self):
        start_date, end_date = date_utils.get_quarter(fields.Date.today())
        rec = {}
        quarter_lead_count = self.env["crm.lead"].search_count(
            [('type', '=', 'lead'),
             ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])

        quarter_opp_count = self.env["crm.lead"].search_count(
            [('type', '=', 'opportunity'),
             ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])

        quarter_expected_revenue = sum(
            self.env["crm.lead"].search([
                                         ('create_date', '>=', start_date),
                                         ('create_date', '<=',
                                          end_date)]).mapped(
                "expected_revenue"))

        quarter_revenue = round(
            sum(self.env["sale.order"].search(
                [('user_id', '=', self.env.user.id),
                 ('create_date', '>=', start_date),
                 ('create_date', '<=', end_date)]).mapped("amount_total")),
            2)

        quarter_win_count = (self.env["crm.lead"]).search_count(
            [('stage_id.is_won', '=', True),
             ('create_date', '>=', start_date),
             ('create_date', '<=', end_date)])
        quarter_win_ratio = round((quarter_win_count / (
                    quarter_lead_count + quarter_opp_count)) * 100, 2)
        rec.update({
            "quarter_lead_count": quarter_lead_count,
            "quarter_opp_count": quarter_opp_count,
            "quarter_expected_revenue": quarter_expected_revenue,
            "quarter_revenue": quarter_revenue,
            "quarter_win_ratio": quarter_win_ratio,
        })

        return rec
