from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_invoiced_amount = fields.Monetary(
        string="Total Invoiced Amount",
        compute="_compute_total_invoiced_amount",
        store=False,
        readonly=True
    )

    @api.depends('partner_id')
    def _compute_total_invoiced_amount(self):
        for order in self:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', order.partner_id.id),
                ('state', 'in', ['posted', 'draft']),
                ('move_type', '=', 'out_invoice')
            ])
            total_amount = sum(invoices.mapped('amount_total'))
            order.total_invoiced_amount = total_amount

