# Copyright (c) 2023, Tech Ventures and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from general_voucher.general_voucher.doctype.utils_functions import get_doctype_by_field


class BankPaymentVoucher(Document):
    def before_submit(self):
        je_present = get_doctype_by_field('Journal Entry', 'bill_no', self.name)
        company = frappe.defaults.get_defaults().company
        bank_account = self.account
        posting_date = self.posting_date
        voucher_type = "Bank Entry"
        crv_no = self.name
        cheque_no = crv_no
        cheque_date = posting_date
        total = self.total
        if len(self.items) > 0 and int(self.bpv_status) < 1 and not je_present:
            je = frappe.new_doc("Journal Entry")
            je.posting_date = posting_date
            je.voucher_type = voucher_type
            je.company = company
            je.bill_no = crv_no
            je.cheque_no = cheque_no,
            je. cheque_date = cheque_date,
            for item in self.items:
                je.append("accounts", {
                    'account': item.account,
                    'party_type': item.party_type,
                    'party': item.party,
                    'user_remark': f"{item.description}, Ref:{item.ref_no}",
                    'debit_in_account_currency': item.amount,
                    'credit_in_account_currency': 0

                })
                je.append("accounts", {
                    'account': bank_account,
                    'debit_in_account_currency': 0,
                    'user_remark': f"{item.description}, Ref:{item.ref_no}",
                    'credit_in_account_currency': item.amount,
                })
            je.submit()
            frappe.db.set_value('Bank Payment Voucher', self.name, 'bpv_status', 1)
        else:
            if len(self.items) < 1:
                frappe.throw("No detailed rows found")
            if self.crv_status > 0:
                frappe.throw("Journal entry already created")

    def on_cancel(self):
        current_je = get_doctype_by_field('Journal Entry', 'bill_no', self.name)
        if current_je.docstatus != 2:  # Ensure the document is in the "Submitted" state
            current_je.cancel()
            frappe.db.commit()
        else:
            frappe.throw("Document is not in the 'Submitted' state.")
        if current_je.amended_from:
            new_name = int(current_je.name.split("-")[-1]) + 1
        else:
            new_name = f"{current_je.name}-{1}"
        make_autoname(new_name, 'Jouranl Entry')
