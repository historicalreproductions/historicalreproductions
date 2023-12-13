from odoo import models,fields,api,_ 
from odoo.exceptions import UserError
import io
import base64

class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    check_moves_for_location_kardex = fields.Boolean(compute="_check_moves_for_location_kardex", string='moves have atleast 1 kardex location', default=False)
    
    # Function to check the move_lines for atleast 1 kardex checkbox to show button in view or not
    def _check_moves_for_location_kardex(self):
        self.check_moves_for_location_kardex = False
        for move in self.move_lines:
            for line in move.move_line_ids:
                if line.location_id.is_kardex_location:
                    self.check_moves_for_location_kardex = True

    # Action to send mail to designed customer and post mail into the chatter to track
    def action_stock_move_send(self):
        template_id = self._find_mail_template()
        if template_id:
            attachment_data = self.generate_txt_file()
            self.message_post(
                body=template_id.body_html,
                subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment'),
                attachment_ids=attachment_data
            )
        else:
            raise UserError('Email Template not found')

    # Function to find correct Email Template configured in the system paramaeters 
    def _find_mail_template(self):
        self.ensure_one()
        template_id = False
        if self.state in ['assigned', 'draft']:
        #if (self.state == 'assigned') or (self.state == 'draft'):
            template_id = self.env['ir.config_parameter'].sudo().get_param('stock.default_kardex_template_id')
            template_id = self.env['mail.template'].search([('name', '=', template_id)])
        return template_id

    # Function to generate a txt file to attach to email which is send to kardex
    def generate_txt_file(self):
        self.ensure_one()
        txt_data = []
        # Structure of txt file "Ordernumber|default_code of the product|quantity|DirectionType|description of the product|Lot|Serialnumber|Customername"
        for move in self.move_lines:
            for line in move.move_line_ids:
                if line.location_id.is_kardex_location:
                    delivery_order_name = self.name
                    customer_name = self.partner_id.name
                    product_code = line.product_id.default_code
                    quantity = line.product_uom_qty
                    product_desc = line.product_id.name
                    lot_nr = line.lot_id.name
                    dir_type = "1"
                    if lot_nr is False:
                        lot_nr = ''
                    txt_data.append(
                        str(delivery_order_name) + 
                        "|" + str(product_code) + 
                        "|" + str(quantity) + 
                        "|" + dir_type + 
                        "|" + str(product_desc) + 
                        "|" + str(lot_nr) + 
                        "|" + str(lot_nr) + 
                        "|" + str(customer_name))
                else:
                    continue
        file_content = "\n".join(txt_data)
        # Logic for naming the txt file
        if self.company_id.is_mandant_01 == True:
            prefix_txt_file_name = 'M01_'
            txt_file_name = prefix_txt_file_name + delivery_order_name + '.txt'
        elif self.company_id.is_mandant_02 == True:
            prefix_txt_file_name = 'M02_'
            txt_file_name = prefix_txt_file_name + delivery_order_name + '.txt'
        else:
            raise UserError('Mandant is not set. Please configure the mandant for your Company in the General Settings!')
        # Attach txt file to email
        attachment = self.env['ir.attachment'].create({
            'name': txt_file_name,
            'datas': base64.encodestring(file_content.encode()),
            'datas_fname': txt_file_name,
            'res_model': 'stock.picking',
            'res_id': self.id,
            'type': 'binary'
        })
        template_id = self._find_mail_template()
        # Deleting existing attachments created from this function before
        template_id.attachment_ids.unlink()
        if not template_id.attachment_ids:
            template_id.attachment_ids = [attachment.id]
        else:
            template_id.attachment_ids = [(4, attachment.id)]
        return [attachment.id]

