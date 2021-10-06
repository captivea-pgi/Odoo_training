# coding: utf-8

from odoo import api, models, fields
from odoo.exceptions import UserError
import logging
from odoo.tools.translate import _
from datetime import datetime

models_to_check = ['helpdesk.ticket']
_logger = logging.getLogger(__name__)

class CapMailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        '''
        ATTENTION : inherit create method may impact the server performance
        Create and write methods have recurrent call on Odoo it means the code inside this function will be
        called a lot of times. (poor english :s)
        :param values:
        :return:
        '''
        message = super(CapMailMessage, self).create(values)
        
        if message.model in models_to_check and message.message_type == 'email':
            _logger.info("We are in the if")
            # check if all variables are True (we need these variable along the code)
            check_variables = all([message.author_id, message.author_id, message.res_id, message.model])
            _logger.info("The check_variables is = %s" % check_variables)
            # if check_variables:
            
            #Link between the helpdesk.ticket model and the message's id
            linked_object = self.env[message.model].sudo().search([('id', '=', message.res_id)])
            _logger.info("The link objet is = %s" % linked_object)
                
            #check which team is linked to the ticket
            equipe = linked_object.team_id
            _logger.info("The equipe is = %s" % equipe)
            
            #look for the min stage id for the group
            etape=min(self.env['helpdesk.stage'].sudo().search([('team_ids', 'in', equipe.id)]))
            _logger.info("The etape is = %s" % etape)

            #same as linked_object = stage_id
            linked_object.write({'stage_id': etape.id})

        return message
