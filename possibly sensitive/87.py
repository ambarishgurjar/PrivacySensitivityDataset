

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"

    online_bank_statement_provider = fields.Selection(
        selection=lambda self: self.env[
            "account.journal"
        ]._selection_online_bank_statement_provider(),
        help="Select the type of service provider (a model)",
    )
    online_bank_statement_provider_id = fields.Many2one(
        string="Statement Provider",
        comodel_name="online.bank.statement.provider",
        ondelete="restrict",
        copy=False,
        help="Select the actual instance of a configured provider (a record).\n"
        "Selecting a type of provider will automatically create a provider"
        " record linked to this journal.",
    )

    def __get_bank_statements_available_sources(self):
        result = super().__get_bank_statements_available_sources()
        result.append(("online", _("Online (OCA)")))
        return result

    @api.model
    def _selection_online_bank_statement_provider(self):
        return self.env["online.bank.statement.provider"]._get_available_services() + [
            ("dummy", "Dummy")
        ]

    @api.model
    def values_online_bank_statement_provider(self):

        res = self.env["online.bank.statement.provider"]._get_available_services()
        if self.user_has_groups("base.group_no_one"):
            res += [("dummy", "Dummy")]
        return res

    def _update_online_bank_statement_provider_id(self):

        OnlineBankStatementProvider = self.env["online.bank.statement.provider"]
        for journal in self.filtered("id"):
            provider_id = journal.online_bank_statement_provider_id
            if journal.bank_statements_source != "online":
                journal.online_bank_statement_provider_id = False
                if provider_id:
                    provider_id.unlink()
                continue
            if provider_id.service == journal.online_bank_statement_provider:
                continue