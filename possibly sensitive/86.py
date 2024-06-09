
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountStatementImport(models.TransientModel):
    _inherit = "account.statement.import"

    paypal_mapping_id = fields.Many2one(
        string="PayPal mapping",
        comodel_name="account.statement.import.paypal.mapping",
    )

    def _parse_file(self, data_file):
        self.ensure_one()
        if self.paypal_mapping_id:
            try:
                Parser = self.env["account.statement.import.paypal.parser"]
                return Parser.parse(
                    self.paypal_mapping_id, data_file, self.statement_filename
                )
            except Exception:
                if self.env.context.get("account_statement_import_paypal_test"):
                    raise
                _logger.warning("PayPal parser error", exc_info=True)
        return super()._parse_file(data_file)
