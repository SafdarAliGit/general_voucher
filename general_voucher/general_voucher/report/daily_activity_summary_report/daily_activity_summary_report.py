# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def decimal_format(value, decimals):
    formatted_value = "{:.{}f}".format(value, decimals)
    return formatted_value


def get_columns():
    columns = [
        {
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "Link",
            "options": "DocType",
            "width": 120
        },
              
        
        {
            "label": _("Debit"),
            "fieldname": "debit",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Credit"),
            "fieldname": "credit",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Grand Total"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 120
        }
    

    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("from_date"):
        conditions.append(f"`{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`{doctype}`.posting_date <= %(to_date)s")

    if doctype == "Journal Entry":
        conditions.append("`tabJournal Entry`.is_opening = 0")

    return " AND ".join(conditions)


def get_account_type_from_name(account_name):
    try:
        account_doc = frappe.get_doc("Account", account_name)
        account_type = account_doc.account_type
        return account_type
    except frappe.DoesNotExistError:
        return None


def get_data(filters):
    data = []

    sale_query = """
    SELECT
        SUM(si.total) AS debit,
        SUM(si.total_taxes_and_charges) AS total_taxes_and_charges,
        SUM(si.grand_total) AS grand_total
    FROM
        `tabSales Invoice` AS si
    WHERE
        {conditions} AND si.docstatus = 1
    
    ORDER BY
        si.posting_date ASC, si.name ASC
    """.format(conditions=get_conditions(filters, "si"))

    purchase_query = """
    SELECT
        SUM(pi.total) AS credit,
        SUM(pi.total_taxes_and_charges) AS total_taxes_and_charges,
        SUM(pi.grand_total) AS grand_total
    FROM
        `tabPurchase Invoice` AS pi
    WHERE
        {conditions} AND pi.docstatus = 1
    ORDER BY
        pi.posting_date ASC, pi.name ASC
    """.format(conditions=get_conditions(filters, "pi"))


    cash_receipt_query = """
    SELECT
        SUM(gle.debit) AS debit,
        SUM(gle.credit) AS credit
    FROM
        `tabGL Entry` AS gle
    WHERE
        {conditions}
        AND gle.is_cancelled = 0
        AND gle.debit > 0
        AND EXISTS (
            SELECT 1
            FROM `tabAccount` AS acc
            WHERE acc.name = gle.account
            AND acc.account_type = 'Cash'
        )
    """.format(conditions=get_conditions(filters, "gle"))

    cash_payment_query = f"""
    SELECT 
        SUM(gl.debit) AS debit,
        SUM(gl.credit) AS credit
    FROM 
        `tabGL Entry` AS gl
    JOIN 
        `tabAccount` AS acc ON acc.name = gl.account
    WHERE 
        {get_conditions(filters, "gl")}
        AND gl.is_cancelled = 0
        AND gl.credit > 0
        AND acc.account_type = 'Cash'
	"""


    bank_receipt = f"""
    SELECT 
        SUM(gl.debit) AS debit,
        SUM(gl.credit) AS credit
    FROM 
        `tabGL Entry` AS gl
    JOIN 
        `tabAccount` AS acc ON acc.name = gl.account
    WHERE 
        {get_conditions(filters, "gl")}
        AND gl.is_cancelled = 0
        AND gl.debit > 0
        AND acc.account_type = 'Bank'
	"""


    bank_payment = f"""
    SELECT 
        SUM(gl.debit) AS debit,
        SUM(gl.credit) AS credit
    FROM 
        `tabGL Entry` AS gl
    JOIN 
        `tabAccount` AS acc ON acc.name = gl.account
    WHERE 
        {get_conditions(filters, "gl")}
        AND gl.is_cancelled = 0
        AND gl.credit > 0
        AND acc.account_type = 'Bank'
	"""


    sale_result = frappe.db.sql(sale_query, filters, as_dict=1)
    sale_result[0]['voucher_type'] = "Sales"
    purchase_result = frappe.db.sql(purchase_query, filters, as_dict=1)
    purchase_result[0]['voucher_type'] = "Purchase"
    cash_receipt_result = frappe.db.sql(cash_receipt_query, filters, as_dict=1)
    cash_receipt_result[0]['voucher_type'] = "Cash Receipt"
    cash_payment_result = frappe.db.sql(cash_payment_query, filters, as_dict=1)
    cash_payment_result[0]['voucher_type'] = "Cash Payment"
    bank_receipt_result = frappe.db.sql(bank_receipt, filters, as_dict=1)
    bank_receipt_result[0]['voucher_type'] = "Bank Receipt"
    bank_payment_result = frappe.db.sql(bank_payment, filters, as_dict=1)
    bank_payment_result[0]['voucher_type'] = "Bank Payment"

    #====================TRANSACTION TYPE FILTER====================
    if filters.get('transaction_types') == "All":
        data.extend(sale_result)
        data.extend(purchase_result)
        data.extend(cash_receipt_result)
        data.extend(cash_payment_result)
        data.extend(bank_receipt_result)
        data.extend(bank_payment_result)
    if 'Sales' in filters.get('transaction_types'):
        data.extend(sale_result)
    if 'Purchases' in filters.get('transaction_types'):
        data.extend(purchase_result)
    if 'Cash Receipt' in filters.get('transaction_types'):
        data.extend(cash_receipt_result)
    if 'Cash Payment' in filters.get('transaction_types'):
        data.extend(cash_payment_result)
    if 'Bank Receipt' in filters.get('transaction_types'):
        data.extend(bank_receipt_result)
    if 'Bank Payment' in filters.get('transaction_types'):
        data.extend(bank_payment_result)
        # ====================FILTERS END====================

    return data
