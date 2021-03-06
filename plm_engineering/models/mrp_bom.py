##############################################################################
#
#    OmniaSolutions, Your own solutions
#    Copyright (C) 2010 OmniaSolutions (<http://omniasolutions.eu>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""
Created on 31 Aug 2016

@author: Daniel Smerghetto
"""

from odoo import models
from odoo import fields
from odoo import api
from odoo import _


class MrpBomExtension(models.Model):
    _inherit = 'mrp.bom'

    type = fields.Selection(selection_add=[('ebom', 'Engineering BoM')])
    ebom_source_id = fields.Integer('Source Ebom ID')

    @api.model
    def _get_in_bom(self, pid, sid=False):
        bom_l_type = self.env['mrp.bom.line']
        bom_line_brws_list = bom_l_type.search(
            [('product_id', '=', pid), ('source_id', '=', sid), ('type', '=', 'ebom')])
        if not bom_line_brws_list:
            bom_line_brws_list = bom_l_type.search(
                [('product_id', '=', pid), ('source_id', '=', sid), ('type', '=', 'normal')])
            if not bom_line_brws_list:
                bom_line_brws_list = bom_l_type.search(
                    [('product_id', '=', pid), ('source_id', '=', False), ('type', '=', 'ebom')])
            if not bom_line_brws_list:
                bom_line_brws_list = bom_l_type.search(
                    [('product_id', '=', pid), ('source_id', '=', False), ('type', '=', 'normal')])
                if not bom_line_brws_list:
                    bom_line_brws_list = bom_l_type.search([('product_id', '=', pid), ('type', '=', 'ebom')])
                if not bom_line_brws_list:
                    bom_line_brws_list = bom_l_type.search([('product_id', '=', pid), ('type', '=', 'normal')])
        return bom_line_brws_list

    @api.model
    def _get_bom(self, pid, sid=False):
        if sid is None:
            sid = False
        bom_brws_list = self.search([('product_tmpl_id', '=', pid), ('source_id', '=', sid), ('type', '=', 'ebom')])
        if not bom_brws_list:
            bom_brws_list = self.search(
                [('product_tmpl_id', '=', pid), ('source_id', '=', sid), ('type', '=', 'normal')])
            if not bom_brws_list:
                bom_brws_list = self.search(
                    [('product_tmpl_id', '=', pid), ('source_id', '=', False), ('type', '=', 'ebom')])
                if not bom_brws_list:
                    bom_brws_list = self.search(
                        [('product_tmpl_id', '=', pid), ('source_id', '=', False), ('type', '=', 'normal')])
                    if not bom_brws_list:
                        bom_brws_list = self.search([('product_tmpl_id', '=', pid), ('type', '=', 'ebom')])
                        if not bom_brws_list:
                            bom_brws_list = self.search([('product_tmpl_id', '=', pid), ('type', '=', 'normal')])
        return bom_brws_list

    @api.model
    def SaveStructure(self, relations, level=0, curr_level=0, kind_bom='ebom'):
        """
            Save EBom relations
        """
        return super(MrpBomExtension, self).SaveStructure(relations, level, curr_level, kind_bom='ebom')
