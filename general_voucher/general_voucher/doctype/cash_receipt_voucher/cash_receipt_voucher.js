frappe.ui.form.on('Cash Receipt Voucher', {

    refresh: function (frm) {
        function calculate_net_total(frm) {
            var amount = 0;
            $.each(frm.doc.items || [], function (i, d) {
                amount += flt(d.amount);
            });
            frm.set_value("total", amount)
        }

        calculate_net_total(frm)

        frm.set_query("account", function () {
            return {
                filters: [
                    ["Account", "account_type", "in", ["Cash"]],
                    ["is_group", "=", 0],
                    ["company", "=", frm.doc.company]
                ]
            };
        });
        frm.set_query('account', 'items', function (doc, cdt, cdn) {
            return {
                filters: [
                    ["Account", "company", "=", frm.doc.company],
                ]
            };
        });

    },

    account: function (frm) {
        frappe.call({
            method: 'general_voucher.general_voucher.doctype.utils.get_account_balance',
            args: {
                account: frm.doc.account,
                company: frm.doc.company
            },
            callback: function (r) {
                if (!r.exc) {
                    frm.set_value('balance', r.message.balance);
                }
            }
        });
    }
});


frappe.ui.form.on("Cash Receipt Voucher Items", {

    account: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.call({
            method: 'general_voucher.general_voucher.doctype.utils.get_party_type',
            args: {
                account: d.account,
            },
            callback: function (r) {
                if (!r.exc) {
                    frappe.model.set_value(cdt, cdn, 'party_type', r.message.party_type);
                }
            }
        });

    },
    amount: function (frm, cdt, cdn) {
        function calculate_net_total(frm) {
            var amount = 0;
            $.each(frm.doc.items || [], function (i, d) {
                amount += flt(d.amount);
            });
            frm.set_value("total", amount)
        }

        calculate_net_total(frm)
    },
    items_remove: function (frm) {
        function calculate_net_total(frm) {
            var amount = 0;
            $.each(frm.doc.items || [], function (i, d) {
                amount += flt(d.amount);
            });
            frm.set_value("total", amount)
        }

        calculate_net_total(frm)
        frm.refresh_field('items');
    }
});

