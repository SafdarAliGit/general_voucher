# Copyright (c) 2023, Tech Ventures and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document


class CashReceiptVoucher(Document):
    def before_submit(self):
        company = frappe.defaults.get_defaults().company
        cash_account = self.account
        posting_date = self.posting_date
        voucher_type = "Cash Entry"
        crv_no = self.name
        total = self.total
        if len(self.items) > 0 and int(self.crv_status) < 1:
            je = frappe.new_doc("Journal Entry")
            je.posting_date = posting_date
            je.voucher_type = voucher_type
            je.company = company
            je.bill_no = crv_no
            je.append("accounts", {
                'account': cash_account,
                'debit_in_account_currency': total,
                'credit_in_account_currency': 0,
            })
            for item in self.items:
                je.append("accounts", {
                    'account': item.account,
                    'party_type': item.party_type,
                    'party': item.party,
                    'user_remark': item.ref_no,
                    'debit_in_account_currency': 0,
                    'credit_in_account_currency': item.amount

                })
            je.submit()
            frappe.db.set_value('Cash Receipt Voucher', self.name, 'crv_status', 1)
        else:
            if len(self.items) < 1:
                frappe.throw("No detailed rows found")
            if self.crv_status > 0:
                frappe.throw("Journal entry already created")
