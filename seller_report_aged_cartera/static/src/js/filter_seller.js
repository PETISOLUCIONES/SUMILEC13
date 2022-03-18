odoo.define('seller_report_aged.filter_seller', function (require) {
'use strict';
console.log("Entrando a la función");
var report = require('account_reports.account_report');
var core = require('web.core');
var datepicker = require('web.datepicker');
var StandaloneFieldManagerMixin = require('web.StandaloneFieldManagerMixin');
var Widget = require('web.Widget');
var field_utils = require('web.field_utils');
var RelationalFields = require('web.relational_fields');
var accountReportsWidget = report.accountReportsWidget;
//var M2MFilters = report.M2MFilters;
var _t = core._t;
var QWeb = core.qweb;
//M2MFilters =  report.M2MFilters.include({});
//ar _super_M2MFilters = report.M2MFilters;

console.log("Creando los filtros ");
var M2MFilters = Widget.extend(StandaloneFieldManagerMixin, {
    /**
     * @constructor
     * @param {Object} fields
     */
    init: function (parent, fields) {
        this._super.apply(this, arguments);
        StandaloneFieldManagerMixin.init.call(this);
        this.fields = fields;
        this.widgets = {};
    },
    /**
     * @override
     */
    willStart: function () {
        var self = this;
        var defs = [this._super.apply(this, arguments)];
        _.each(this.fields, function (field, fieldName) {
            defs.push(self._makeM2MWidget(field, fieldName));
        });
        return Promise.all(defs);
    },
    /**
     * @override
     */
    start: function () {
        var self = this;
        var $content = $(QWeb.render("m2mWidgetTable", {fields: this.fields}));
        self.$el.append($content);
        _.each(this.fields, function (field, fieldName) {
            self.widgets[fieldName].appendTo($content.find('#'+fieldName+'_field'));
        });
        return this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * This method will be called whenever a field value has changed and has
     * been confirmed by the model.
     *
     * @private
     * @override
     * @returns {Promise}
     */
    _confirmChange: function () {
        var self = this;
        var result = StandaloneFieldManagerMixin._confirmChange.apply(this, arguments);
        var data = {};
        _.each(this.fields, function (filter, fieldName) {
            data[fieldName] = self.widgets[fieldName].value.res_ids;
        });
        this.trigger_up('value_changed', data);
        return result;
    },
    /**
     * This method will create a record and initialize M2M widget.
     *
     * @private
     * @param {Object} fieldInfo
     * @param {string} fieldName
     * @returns {Promise}
     */
    _makeM2MWidget: function (fieldInfo, fieldName) {
        var self = this;
        var options = {};
        options[fieldName] = {

            options: {
                no_create_edit: true,
                no_create: true,
            }
        };
        var domain = ""
        /* SE COMENTA AL CAMBIAR DE VENDEDOR EMPLEADO PARA USUARIO
        if (fieldName == "seller_ids"){
            domain = "['|',('department_id','ilike', 'Comercial'), ('department_id','ilike', 'ventas')]"
            }*/
        return this.model.makeRecord(fieldInfo.modelName, [{
            fields: [{
                name: 'id',
                type: 'integer',
            }, {
                name: 'display_name',
                type: 'char',
            }],
            name: fieldName,
            relation: fieldInfo.modelName,
            type: 'many2many',
            domain : domain,
            value: fieldInfo.value,
        }], options).then(function (recordID) {
            self.widgets[fieldName] = new RelationalFields.FieldMany2ManyTags(self,
                fieldName,
                self.model.get(recordID),
                {mode: 'edit',}
            );
            self._registerWidget(recordID, fieldName, self.widgets[fieldName]);
        });
    },
});

report.include({
   // hasControlPanel: true,
///Console.log("Heredando a la función");

     update_cp: function() {
        if (!this.$buttons) {
            this.renderButtons();
        }
        var status = {
            cp_content: {
                $buttons: this.$buttons,
                $searchview_buttons: this.$searchview_buttons,
                $pager: this.$pager,
                $searchview: this.$searchview,
            },
        };
        return this.updateControlPanel(status, {clear: true});
    },
   custom_events: {
        'value_changed': function(ev) {
             var self = this;
             self.report_options.partner_ids = ev.data.partner_ids;
             self.report_options.seller_ids = ev.data.seller_ids;
             self.report_options.partner_categories = ev.data.partner_categories;
             self.report_options.analytic_accounts = ev.data.analytic_accounts;
             self.report_options.analytic_tags = ev.data.analytic_tags;
             return self.reload().then(function () {
                 self.$searchview_buttons.find('.account_partner_filter').click();
                 self.$searchview_buttons.find('.account_analytic_filter').click();
             });
         },
    },
   render_searchview_buttons: function() {


                var self = this;


                // partner filter
        if (this.report_options.partner) {
            if (!this.M2MFilters  ) {
                var fields = {};
                if ('partner_ids' in this.report_options) {
                    fields['partner_ids'] = {
                        label: _t('Partners'),
                        modelName: 'res.partner',
                        value: this.report_options.partner_ids.map(Number),
                    };
                }
				 if ('seller_ids' in this.report_options) {
                    fields['seller_ids'] = {
                        label: _t('Vendedores'),
                        modelName: 'res.users',
                        value: this.report_options.seller_ids.map(Number),
                    };
                }
                if ('partner_categories' in this.report_options) {
                    fields['partner_categories'] = {
                        label: _t('Tags'),
                        modelName: 'res.partner.category',
                        value: this.report_options.partner_categories.map(Number),
                    };
                }
                if (!_.isEmpty(fields)) {
                    this.M2MFilters = new M2MFilters(this, fields);
                    this.M2MFilters.appendTo(this.$searchview_buttons.find('.js_account_partner_m2m'));
                }
            } else {
                this.$searchview_buttons.find('.js_account_partner_m2m').append(this.M2MFilters.$el);
            }
        }



            /*if (this.report_options.seller) {
     if (!this.M2MFilters || !this.M2MFilters.fields.seller_ids) {
                 var fields = {};
                 if (this.M2MFilters ){
                 fields = this.M2MFilters.fields;
                 }


                    if ('seller_ids' in this.report_options) {
                        fields['seller_ids'] = {
                            label: _t('VendedoresPrueba Extendiendo el  js'),
                            modelName: 'hr.employee',
                            value: this.report_options.seller_ids.map(Number)
                        };
    if (!_.isEmpty(fields)) {
                        this.M2MFilters = new M2MFilters(this, fields);
                        this.M2MFilters.appendTo(self.$searchview_buttons.find('.js_account_partner_m2m'));
                            }
                } else {
                    this.$searchview_buttons.find('.js_account_partner_m2m').append(this.M2MFilters.$el);

     }
       }



    } */
    this._super()

    }

});
/*
core.action_registry.add('account_report_filtter', report);

return report;

core.action_registry.add('account_report', report);

return report;
*/
});