require.undef('keyview');

window.inputElement = undefined;

define('keyview', ["jupyter-js-widgets"], function(widgets) {

    var KeyView = widgets.DOMWidgetView.extend({
        render: function() {
            this.el.textContent = '[Do not close this widget]';
            
            document.onkeydown = function(evt) {
                if (window.inputElement === undefined || window.inputElement !== document.activeElement) { return; }
                evt = evt || window.event;
                this.model.set("current_key", "None");
                this.touch();
                this.model.set("current_key", evt.key);
                this.touch();
            }.bind(this);
        }
    });

    return {
        KeyView: KeyView
    }
});