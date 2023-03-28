odoo.define("crm_dashboard.DashboardDashboard", function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var web_client = require('web.web_client');
    var session = require('web.session');
    var ajax = require('web.ajax');
    var _t = core._t;
    var rpc = require('web.rpc');
    var self = this;
    var DashBoard = AbstractAction.extend({
        contentTemplate: 'DashboardDashboard',
        events:{
         'click .my_lead':'my_lead',
         'click .opportunity':'opportunity',
         'change #income_expense_values': function(e) {
            e.stopPropagation();
            var $target = $(e.target);
            var value = $target.val();
            if (value=="this_year"){
                this.onclick_this_year($target.val());
                this.onclick_year();
            }else if (value=="this_quarter"){
                this.onclick_this_quarter($target.val());
            }else if (value=="this_month"){
                this.onclick_this_month($target.val());
                this.onclick_month();
            }else if (value=="this_week"){
                this.onclick_this_week($target.val());
                this.onclick_week();
            }
        },
        },

    init:function(parent, action){
    this._super(parent, action);
    rpc.query({
            model:'crm.lead',
            method:'get_crm_lead',
         }).then(function(result){
            console.log(result)
            $('#my_lead').append('<span>' + result.lead+'</span>');
            $('#opportunity').append('<span>' + result.opportunity+'</span>');
            $('#revenue').append('<span>' + result.revenue+'</span>');
            $('#expected_revenue').append('<span>' + result.expected_revenue+'</span>');
            $('#win_ratio').append('<span>' + result.win_ratio+'</span>');

         })
        },
        start:function(){
            var self = this;
            this.set("title",'dashboard');
            return this._super().then(function(){
            self.render_graph();
            });
          },
        my_lead : function(){
        this.do_action({
                name: _t("My Leads"),
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['user_id', '=', session.uid]],
                target: 'current',
            })
        },
        opportunity : function() {
         this.do_action({
                name: _t("Opportunity"),
                type: 'ir.actions.act_window',
                res_model: 'crm.lead',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['user_id', '=', session.uid], ['type','=', 'opportunity']],
                target: 'current',
            })
        },
        onclick_this_year: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_year',
                args: [],
            }).then(function (result) {
                $('#my_lead').empty()
                $('#opportunity').empty()
                $('#revenue').empty()
                $('#expected_revenue').empty()
                $('#win_ratio').empty()
                $('#my_lead').append('<span>' + result.lead_year+'</span>');
                $('#opportunity').append('<span>' + result.opportunity_year+'</span>');
                $('#revenue').append('<span>' + result.year_revenue+'</span>');
                $('#expected_revenue').append('<span>' + result.expected_rev_year+'</span>');
                $('#win_ratio').append('<span>' + result.year_win_ratio+'</span>');
        })
         },
        onclick_this_month: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_month',
                args: [],
            }).then(function (result) {
                $('#my_lead').empty()
                $('#opportunity').empty()
                $('#revenue').empty()
                $('#expected_revenue').empty()
                $('#win_ratio').empty()
                $('#my_lead').append('<span>' + result.month_lead_count+'</span>');
                $('#opportunity').append('<span>' + result.month_expected_revenue+'</span>');
                $('#revenue').append('<span>' + result.month_revenue+'</span>');
                $('#expected_revenue').append('<span>' + result.month_expected_revenue+'</span>');
                $('#win_ratio').append('<span>' + result.month_win_ratio+'</span>');
            })
            },
         onclick_this_week: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_week',
                args: [],
            }).then(function (result) {
                $('#my_lead').empty()
                $('#opportunity').empty()
                $('#revenue').empty()
                $('#expected_revenue').empty()
                $('#win_ratio').empty()
                $('#my_lead').append('<span>' + result.week_lead_count+'</span>');
                $('#opportunity').append('<span>' + result.week_opp_count+'</span>');
                $('#revenue').append('<span>' + result.week_revenue+'</span>');
                $('#expected_revenue').append('<span>' + result.week_expected_revenue+'</span>');
                $('#win_ratio').append('<span>' + result.week_win_ratio+'</span>');


        })
         },
          onclick_this_quarter: function (ev) {
            var self = this;
            rpc.query({
                model: 'crm.lead',
                method: 'crm_quarter',
                args: [],
            }).then(function (result) {
                $('#my_lead').empty()
                $('#opportunity').empty()
                $('#revenue').empty()
                $('#expected_revenue').empty()
                $('#win_ratio').empty()
                $('#my_lead').append('<span>' + result.quarter_lead_count+'</span>');
                $('#opportunity').append('<span>' +result.quarter_opp_count+'</span>');
                $('#revenue').append('<span>' + result.quarter_revenue+'</span>');
                $('#expected_revenue').append('<span>' + result.quarter_expected_revenue+'</span>');
                $('#win_ratio').append('<span>' + result.quarter_win_ratio+'</span>');
                })
                },
        render_graph :function(){
            var self = this;
            rpc.query({
                model:'crm.lead',
                method:'get_stage_graph',
                }).then(function(result){
            const ctx = self.$(".stage_graph");
            new Chart(ctx, {
            type: 'bar',
            data: {
            labels: result[0],
            datasets: [{
            label: '# Total Lead',
            data: result[1],
            borderWidth: 1
            }]
          },
          options: {
             scales: {
             y: {
               beginAtZero: true
             }
           }
         }
        })
       });

        },
     onclick_year :function(){
      var self = this;
                $('.stage_graph').hide()
                $('.stage_graph_month').hide()
                $(".stage_graph_week").hide()
                $('.stage_graph_quarter').hide()
                $('.stage_graph_year').show()
            rpc.query({
                model:'crm.lead',
                method:'get_stage_graph_year',
                }).then(function(result){
                console.log('year',result)
            const ctx = self.$(".stage_graph_year");
            new Chart(ctx, {
            type: 'bar',
            data: {
            labels: result[0],
            datasets: [{
            label: '# Total Lead Of Year',
            data: result[1],
            borderWidth: 1
            }]
          },
          options: {
             scales: {
             y: {
               beginAtZero: true
             }
           }
         }
        })
       });
     },
     onclick_month :function(){
      var self = this;
                $('.stage_graph').hide()
                $('.stage_graph_month').show()
                $(".stage_graph_week").hide()
                $('.stage_graph_quarter').hide()
                $('.stage_graph_year').hide()
            rpc.query({
                model:'crm.lead',
                method:'get_stage_graph_month',
                }).then(function(result){
                console.log('month',result)
            const ctx = self.$(".stage_graph_month");
            new Chart(ctx, {
            type: 'bar',
            data: {
            labels: result[0],
            datasets: [{
            label: '# Total Lead Of Month',
            data: result[1],
            borderWidth: 1
            }]
          },
          options: {
             scales: {
             y: {
               beginAtZero: true
             }
           }
         }
        })
       });
     },
    onclick_week :function(){
      var self = this;
                $('.stage_graph').hide()
                $('.stage_graph_month').hide()
                $(".stage_graph_week").show()
                $('.stage_graph_quarter').hide()
                $('.stage_graph_year').hide()
            rpc.query({
                model:'crm.lead',
                method:'get_stage_graph_week',
                }).then(function(result){
                console.log('month',result)
            const ctx = self.$(".stage_graph_week");
            new Chart(ctx, {
            type: 'bar',
            data: {
            labels: result[0],
            datasets: [{
            label: '# Total Lead Of Week',
            data: result[1],
            borderWidth: 1
            }]
          },
          options: {
             scales: {
             y: {
               beginAtZero: true
             }
           }
         }
        })
       });
     },
    })

    core.action_registry.add('crm_dashboard', DashBoard);
    return DashBoard;
 });