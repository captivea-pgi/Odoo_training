# coding: utf-8

from odoo import api, models, fields
from odoo.exceptions import UserError
#import logging
from odoo.tools.translate import _
from datetime import datetime

models_to_check = ['helpdesk.ticket']
#_logger = logging.getLogger(__name__)

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
            #Link between the helpdesk.ticket model and the message's id
            linked_object = self.env[message.model].sudo().search([('id', '=', message.res_id)])
                
            #check which team is linked to the ticket
            equipe = linked_object.team_id
            
            #look for the min stage id for the group
            etape=min(self.env['helpdesk.stage'].sudo().search([('team_ids', 'in', equipe.id)]))

            #same as linked_object.stage_id = etape.id
            linked_object.write({'stage_id': etape.id})

        return message
