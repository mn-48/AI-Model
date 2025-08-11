frappe.ui.form.on('Item', {
    refresh(frm) {
        frm.add_custom_button('Ask AI (DB)', function () {
            frappe.prompt(
                [
                    {
                        fieldname: 'prompt',
                        label: 'Your Question',
                        fieldtype: 'Data',
                        reqd: 1
                    }
                ],
                function (values) {
                    frappe.call({
                        method: "my_custom_app.api.ai_database_agent",
                        args: {
                            prompt: values.prompt
                        },
                        callback: function (r) {
                            if (r.message.error) {
                                frappe.msgprint(`Error: ${r.message.error}`);
                            } else {
                                frappe.msgprint(`
                                    <b>SQL:</b> ${r.message.sql} <br><br>
                                    <b>Result:</b> <pre>${JSON.stringify(r.message.result, null, 2)}</pre>
                                `);
                            }
                        }
                    });
                },
                'Ask AI Database Agent',
                'Submit'
            );
        });
    }
});
