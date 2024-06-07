# Copyright 2024 Viindoo Technology Joint Stock Company (Viindoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade

_account_tax_group_xmlid = [
    "l10n_vn.tax_group_0",
    "l10n_vn.tax_group_10",
    "l10n_vn.tax_group_5",
]

_account_tax_xmlid = [
    "l10n_vn.tax_purchase_vat0",
    "l10n_vn.tax_purchase_vat10",
    "l10n_vn.tax_purchase_vat5",
    "l10n_vn.tax_sale_vat0",
    "l10n_vn.tax_sale_vat10",
    "l10n_vn.tax_sale_vat5",
]


def _vn_coa_rename_xml_id(env):
    """
    Since the removal of account.chart.template
    we need to rename some xml_id like tax or tax.group
    in order to avoid duplication
    """
    env.cr.execute(
        """SELECT array_agg(id) FROM res_company WHERE chart_template = 'vn'"""
    )
    xmlids_renames = []
    for company_id in env.cr.fetchall():
        for tax_group_xmlid in _account_tax_group_xmlid:
            old_xmlid = f"l10n_vn.{company_id}_" + tax_group_xmlid.split(".")[1]
            new_xmlid = f"account.{company_id}_" + tax_group_xmlid.split(".")[1]
            xmlids_renames.append((old_xmlid, new_xmlid))
        for tax_xmlid in _account_tax_xmlid:
            old_xmlid = f"l10n_vn.{company_id}_" + tax_xmlid.split(".")[1]
            new_xmlid = f"account.{company_id}_" + tax_xmlid.split(".")[1]
            xmlids_renames.append((old_xmlid, new_xmlid))
    openupgrade.rename_xmlids(env.cr, xmlids_renames)


@openupgrade.migrate()
def migrate(env, version):
    _vn_coa_rename_xml_id(env)
