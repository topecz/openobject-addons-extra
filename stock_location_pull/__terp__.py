##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

{
    'name': 'Create Stock Location Paths within Warehouses',
    'version': '1.0',
    'category': 'Generic Modules/Inventory Control',
    'description': """
Manages product's path in locations.

This module may be useful for different purposes:
* Manages the product in his whole manufacturing chain
* Manages different default locations by products
* Define paths within the warehouse to route products based on operations:
   - Quality Control
   - After Sales Services
   - Supplier Return
* Manage products to be rent.
    """,
    'author': 'Tiny',
    'depends': ['mrp_procurement','stock'],
    'init_xml': [],
    'update_xml': ['stock_view.xml', 'security/ir.model.access.csv', 'mrp_pull_workflow.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '9872448400349',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
