odoo.define('muk_web_theme.ActionManager', function (require) {
"use strict";

const ActionManager = require('web.ActionManager');

ActionManager.include({
    _handleAction(action) {
        return this._super(...arguments).then($.proxy(this, '_hideMenusByAction', action));
    },
    _hideMenusByAction(action) {
        const unique_selection = '[data-action-id=' + action.id + ']';
        $(_.str.sprintf('.o_menu_sections.show:has(%s)', unique_selection)).collapse('hide');
        $('.o_menu_apps .dropdown-menu.show').removeClass('show');
    },
});

});
