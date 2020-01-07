# © 2018 Yasmany Castillo <yasmany003@gmail.com>

import logging

from odoo import models, api

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order.
         This method may be overridden to implement custom invoice generation
         (making sure to call super() to establish a clean extension chain).
        """
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        journal_id = self.env['account.journal'].browse(
            invoice_vals['journal_id'])
        if not journal_id.l10n_do_fiscal_journal:
            return invoice_vals

        partner_id = self.partner_id
        fiscal_type_id = partner_id.sale_fiscal_type_id

        if partner_id.parent_id and partner_id.parent_id.is_company:
            invoice_vals[
                'fiscal_type_id'] = partner_id.parent_id.sale_fiscal_type_id
        elif not fiscal_type_id and partner_id.vat and partner_id.is_company:
            invoice_vals['fiscal_type_id'] = 'fiscal'
        else:
            invoice_vals['fiscal_type_id'] = fiscal_type_id

        return invoice_vals
