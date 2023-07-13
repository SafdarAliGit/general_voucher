frappe.ui.form.on('Cash Payment Voucher', {

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
                    ["is_group", "not in", [1]]
                ]
            };
        });
    },
    account: function (frm) {
        frappe.call({
            method: 'general_voucher.general_voucher.doctype.utils.get_account_balance',
            args: {
                account: frm.doc.account,
            },
            callback: function (r) {
                if (!r.exc) {
                    frm.set_value('balance', r.message.balance);
                }
            }
        });
    }
});


frappe.ui.form.on("Cash Payment Voucher Items", {

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

