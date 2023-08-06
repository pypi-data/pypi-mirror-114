odoo.define('muk_web_theme.kanban_column_quick_create', function (require) {
"use strict";

const config = require('web.config');

const KanbanRenderer = require('web.kanban_column_quick_create');

KanbanRenderer.include({
    init() {
        this._super(...arguments);
        this.isMobile = config.device.isMobile;
    },
    _cancel() {
    	if (!config.device.isMobile) {
    		this._super(...arguments);
    	} else if (!this.folded) {
            this.$input.val('');
        }
    },
});

});
