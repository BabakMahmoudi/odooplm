# -*- encoding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Open Source Management Solution    
#    Copyright (C) 2010-2011 OmniaSolutions (<http://www.omniasolutions.eu>). All Rights Reserved
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

'''
Created on Apr 19, 2017

@author: daniel
'''

import logging
import tempfile
import os
import base64
from odoo import models
from odoo import fields
from odoo import api
from odoo import _


class ResGroups(models.Model):
    _name = 'res.groups'
    _inherit = 'res.groups'

    custom_procedure = fields.Binary(string=_('Client CustomProcedure'))
    custom_procedure_fname = fields.Char(_("New File name"))
    custom_read_content = fields.Text('Modif Content', default='')

    @api.multi
    def getCustomProcedure(self):
        for groupBrws in self:
            logging.info('Request CustomProcedure file for user %r and group %r-%r and id %r' % (groupBrws.env.uid, groupBrws.category_id.name, groupBrws.name, groupBrws.id))
            if groupBrws.custom_procedure:
                return True, groupBrws.custom_procedure, groupBrws.custom_procedure_fname
        return False, '', groupBrws.custom_procedure_fname

    @api.multi
    def open_custommodule_edit(self):
        for groupBrws in self:
            self.commonCustomEdit(groupBrws.custom_procedure)
            
    @api.model
    def commonCustomEdit(self, fileContent):
        if fileContent:
            fileReadableContent = base64.decodestring(fileContent)
            self.custom_read_content = fileReadableContent
    
    @api.multi
    def open_custommodule_save(self):
        for groupBrws in self:
            groupBrws.custom_procedure = base64.encodestring(self.custom_read_content.encode('utf-8'))
            tmpFolder = tempfile.gettempdir()
            if groupBrws.custom_procedure_fname:
                customFilePath = os.path.join(tmpFolder, groupBrws.custom_procedure_fname)
                with open(customFilePath, 'wb') as writeFile:
                    writeFile.write(base64.decodestring(groupBrws.custom_procedure))
            groupBrws.custom_read_content = ''
        
ResGroups()
