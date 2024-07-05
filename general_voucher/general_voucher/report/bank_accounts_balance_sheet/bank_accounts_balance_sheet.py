import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), []

    if filters.account:
        accounts_list = frappe.db.get_list("Account", {"is_group": 0, "parent_account": filters.account}, pluck="name")
    else:
        accounts_list = frappe.db.get_list("Account", {"is_group": 0}, pluck="name")

    if not accounts_list:
        frappe.throw(_("No accounts found under the specified conditions."))

    accounts = ", ".join("'"+acc+"'" for acc in accounts_list)
    conditions = get_conditions(filters)
    gl_entries = frappe.db.sql("""
        select account, SUM(debit) as debit, SUM(credit) as credit, SUM(debit - credit) as balance
        from `tabGL Entry`
        where is_cancelled = 0 and account in ({0}) {1}
        group by account
        order by account
    """.format(accounts, conditions), as_dict=True, debug=True)

    data = gl_entries
    return columns, data

def get_conditions(filters):
    cond = ""
    if filters and filters.company:
        cond += " and company = '{0}'".format(filters.company)

    return cond

def get_columns():
    columns = [
        {
            "fieldname": "account",
            "fieldtype": "Link",
            "options": "Account",
            "label": _("Bank Account"),
            "width": 300,
        },
        {
            "fieldname": "debit",
            "fieldtype": "Currency",
            "label": _("Amount In"),
            "width": 200
        },
        {
            "fieldname": "credit",
            "fieldtype": "Currency",
            "label": _("Amount Out"),
            "width": 200
        },
        {
            "fieldname": "balance",
            "fieldtype": "Currency",
            "label": _("Balance"),
            "width": 200,
        }
    ]

    return columns
