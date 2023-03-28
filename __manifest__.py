{'name': 'CRM Dashboard',
 'version': '16.0.1.0.0',
 'sequence': -1,
 'category': 'all',
 'installable': True,
 'application': True,
 'auto_install': False,
 'depends': ['base', 'crm', 'sale'],
 'data':[
  'views/sale_team_inherit.xml',
  'views/dash_board_menu.xml'
 ],
'assets': {
   'web.assets_backend': [
       'crm_dashboard/static/src/xml/dashboard_template.xml',
       'crm_dashboard/static/src/js/dash_board.js',
       'crm_dashboard/static/src/css/tiels_style.scss',
       'https://cdn.jsdelivr.net/npm/chart.js',
   ]}
 }
