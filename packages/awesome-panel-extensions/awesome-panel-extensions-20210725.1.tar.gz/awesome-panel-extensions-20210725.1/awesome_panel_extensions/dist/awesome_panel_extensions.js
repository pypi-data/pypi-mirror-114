/*!
 * Copyright (c) 2012 - 2021, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */
(function(root, factory) {
  factory(root["Bokeh"], undefined);
})(this, function(Bokeh, version) {
  var define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" && (version != null ? Bokeh[version] : Bokeh);
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh " + version + ". You have to load it prior to loading plugins.");
    }
  })
({
"ed583be1cf": /* index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const AwesomePanelExtensions = tslib_1.__importStar(require("ea89eb96d7") /* ./bokeh_extensions */);
    exports.AwesomePanelExtensions = AwesomePanelExtensions;
    const base_1 = require("@bokehjs/base");
    base_1.register_models(AwesomePanelExtensions);
},
"ea89eb96d7": /* bokeh_extensions\index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    var fast_anchor_1 = require("3ab92f5894") /* ./fast/fast_anchor */;
    __esExport("FastAnchor", fast_anchor_1.FastAnchor);
    var fast_button_1 = require("1d9a6373ec") /* ./fast/fast_button */;
    __esExport("FastButton", fast_button_1.FastButton);
    var fast_checkbox_group_1 = require("b62557482c") /* ./fast/fast_checkbox_group */;
    __esExport("FastCheckboxGroup", fast_checkbox_group_1.FastCheckboxGroup);
    var fast_switch_group_1 = require("b714a2453d") /* ./fast/fast_switch_group */;
    __esExport("FastSwitchGroup", fast_switch_group_1.FastSwitchGroup);
    var fast_textarea_input_1 = require("e9b1cd48b7") /* ./fast/fast_textarea_input */;
    __esExport("FastTextAreaInput", fast_textarea_input_1.FastTextAreaInput);
    var fast_text_input_1 = require("92a4b5b2b8") /* ./fast/fast_text_input */;
    __esExport("FastTextInput", fast_text_input_1.FastTextInput);
    var pivot_table_1 = require("eb2d75c5b0") /* ./pivot_table */;
    __esExport("PivotTable", pivot_table_1.PivotTable);
    var icon_1 = require("5f262d0d3a") /* ./icon */;
    __esExport("Icon", icon_1.Icon);
    var web_component_1 = require("514b75040d") /* ./web_component */;
    __esExport("WebComponent", web_component_1.WebComponent);
},
"3ab92f5894": /* bokeh_extensions\fast\fast_anchor.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    class FastAnchorView extends html_box_1.HTMLBoxView {
        setAttr(attribute, value) {
            const anchor_el = this.anchor_el;
            if (value === null) {
                anchor_el.setAttribute(attribute, false);
            }
            else {
                anchor_el.setAttribute(attribute, value);
            }
        }
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.name.change, () => {
                if (this.model.name === null) {
                    this.anchor_el.innerHTML = "";
                }
                else {
                    this.anchor_el.innerHTML = this.model.name;
                }
            });
            this.connect(this.model.properties.appearance.change, () => {
                this.setAttr("appearance", this.model.appearance);
            });
            this.connect(this.model.properties.href.change, () => {
                this.setAttr("href", this.model.href);
            });
            this.connect(this.model.properties.hreflang.change, () => {
                this.setAttr("hreflang", this.model.hreflang);
            });
            this.connect(this.model.properties.ping.change, () => {
                this.setAttr("ping", this.model.ping);
            });
            this.connect(this.model.properties.href.change, () => {
                this.setAttr("referrerpolicy", this.model.referrerpolicy);
            });
            this.connect(this.model.properties.download.change, () => {
                this.setAttr("download", this.model.download);
            });
            this.connect(this.model.properties.referrer.change, () => {
                this.setAttr("referrer", this.model.referrer);
            });
            this.connect(this.model.properties.rel.change, () => {
                this.setAttr("rel", this.model.rel);
            });
            this.connect(this.model.properties.target.change, () => {
                this.setAttr("mimetype", this.model.mimetype);
            });
        }
        render() {
            super.render();
            const anchor_el = document.createElement("fast-anchor");
            this.anchor_el = anchor_el;
            this.anchor_el.style.width = "100%";
            this.el.appendChild(this.anchor_el);
            if (this.model.name !== null) {
                this.anchor_el.innerHTML = this.model.name;
            }
            if (this.model.appearance !== null) {
                anchor_el.appearance = this.model.appearance;
            }
            if (this.model.href !== null) {
                anchor_el.href = this.model.href;
            }
            if (this.model.hreflang !== null) {
                anchor_el.hreflang = this.model.hreflang;
            }
            if (this.model.ping !== null) {
                anchor_el.ping = this.model.ping;
            }
            if (this.model.referrerpolicy !== null) {
                anchor_el.referrerpolicy = this.model.referrerpolicy;
            }
            if (this.model.download !== null) {
                anchor_el.download = this.model.download;
            }
            if (this.model.referrer !== null) {
                anchor_el.ref = this.model.referrer;
            }
            if (this.model.rel !== null) {
                anchor_el.rel = this.model.rel;
            }
            if (this.model.target !== null) {
                anchor_el.target = this.model.target;
            }
            if (this.model.mimetype !== null) {
                anchor_el.mimetype = this.model.mimetype;
            }
        }
    }
    exports.FastAnchorView = FastAnchorView;
    FastAnchorView.__name__ = "FastAnchorView";
    class FastAnchor extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_FastAnchor() {
            this.prototype.default_view = FastAnchorView;
            this.define(({ String }) => ({
                appearance: [String,],
                download: [String,],
                href: [String,],
                hreflang: [String,],
                ping: [String,],
                referrerpolicy: [String,],
                referrer: [String,],
                rel: [String,],
                target: [String,],
                mimetype: [String,],
            }));
        }
    }
    exports.FastAnchor = FastAnchor;
    FastAnchor.__name__ = "FastAnchor";
    FastAnchor.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_anchor";
    FastAnchor.init_FastAnchor();
},
"1d9a6373ec": /* bokeh_extensions\fast\fast_button.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const button_1 = require("@bokehjs/models/widgets/button");
    // Browse the fast-button api here  https://explore.fast.design/components/fast-button
    class FastButtonView extends button_1.ButtonView {
        _render_button(..._) {
            const button = document.createElement("fast-button");
            button.innerText = this.model.label;
            button.disabled = this.model.disabled;
            button.appearance = this.model.appearance;
            button.autofocus = this.model.autofocus;
            button.style.width = "100%";
            button.style.height = "100%";
            return button;
        }
    }
    exports.FastButtonView = FastButtonView;
    FastButtonView.__name__ = "FastButtonView";
    class FastButton extends button_1.Button {
        // __view_type__: FastButtonView
        constructor(attrs) {
            super(attrs);
        }
        static init_FastButton() {
            this.prototype.default_view = FastButtonView;
            this.define(({ Boolean, String }) => ({
                appearance: [String, "neutral"],
                autofocus: [Boolean, false],
            }));
        }
    }
    exports.FastButton = FastButton;
    FastButton.__name__ = "FastButton";
    FastButton.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_button";
    FastButton.init_FastButton();
},
"b62557482c": /* bokeh_extensions\fast\fast_checkbox_group.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const checkbox_group_1 = require("@bokehjs/models/widgets/checkbox_group");
    const inputs = tslib_1.__importStar(require("@bokehjs/styles/widgets/inputs.css"));
    const dom_1 = require("@bokehjs/core/dom");
    const array_1 = require("@bokehjs/core/util/array");
    // Browse the fast-button api here  https://explore.fast.design/components/fast-button
    class FastCheckboxGroupView extends checkbox_group_1.CheckboxGroupView {
        render() {
            // Cannot call super.render() as this will add the group twice
            // super.render()
            const group = dom_1.div({ class: [inputs.input_group, this.model.inline ? inputs.inline : null] });
            this.el.innerHTML = "";
            this.el.appendChild(group);
            const { active, labels } = this.model;
            this._inputs = [];
            for (let i = 0; i < labels.length; i++) {
                let fastCheckBox = document.createElement("fast-checkbox");
                if (this.model.readonly)
                    // Setting the property did not work for me. Thus I set the attribute
                    fastCheckBox.setAttribute("readonly", true);
                fastCheckBox.innerHTML = labels[i];
                const checkbox = fastCheckBox;
                checkbox.value = `${i}`;
                // const checkbox = input({type: `checkbox`, value: `${i}`})
                checkbox.addEventListener("change", () => this.change_active(i));
                this._inputs.push(checkbox);
                if (this.model.disabled)
                    checkbox.disabled = true;
                if (array_1.includes(active, i))
                    checkbox.checked = true;
                // const label_el = label({}, checkbox, span({}, labels[i]))
                group.appendChild(checkbox);
            }
        }
    }
    exports.FastCheckboxGroupView = FastCheckboxGroupView;
    FastCheckboxGroupView.__name__ = "FastCheckboxGroupView";
    class FastCheckboxGroup extends checkbox_group_1.CheckboxGroup {
        constructor(attrs) {
            super(attrs);
        }
        static init_FastCheckboxGroup() {
            this.prototype.default_view = FastCheckboxGroupView;
            this.define(({ Boolean }) => ({
                readonly: [Boolean,],
            }));
        }
    }
    exports.FastCheckboxGroup = FastCheckboxGroup;
    FastCheckboxGroup.__name__ = "FastCheckboxGroup";
    FastCheckboxGroup.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_checkbox_group";
    FastCheckboxGroup.init_FastCheckboxGroup();
},
"b714a2453d": /* bokeh_extensions\fast\fast_switch_group.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const checkbox_group_1 = require("@bokehjs/models/widgets/checkbox_group");
    const inputs = tslib_1.__importStar(require("@bokehjs/styles/widgets/inputs.css"));
    const dom_1 = require("@bokehjs/core/dom");
    const array_1 = require("@bokehjs/core/util/array");
    // Browse the fast-switch api here https://explore.fast.design/components/fast-switch
    class FastSwitchGroupView extends checkbox_group_1.CheckboxGroupView {
        render() {
            // Cannot call super.render() as this will add the group twice
            // super.render()
            const group = dom_1.div({ class: [inputs.input_group, this.model.inline ? inputs.inline : null] });
            this.el.innerHTML = "";
            this.el.appendChild(group);
            const { active, labels } = this.model;
            this._inputs = [];
            for (let i = 0; i < labels.length; i++) {
                let FastSwitch = document.createElement("fast-switch");
                if (this.model.readonly)
                    // Setting the property did not work for me. Thus I set the attribute
                    FastSwitch.setAttribute("readonly", true);
                FastSwitch.innerHTML = labels[i];
                FastSwitch.innerHTML = labels[i];
                const fastSwitch = FastSwitch;
                fastSwitch.value = `${i}`;
                // const checkbox = input({type: `checkbox`, value: `${i}`})
                fastSwitch.addEventListener("change", () => this.change_active(i));
                this._inputs.push(fastSwitch);
                if (this.model.disabled)
                    fastSwitch.disabled = true;
                if (array_1.includes(active, i))
                    fastSwitch.checked = true;
                const checked_message = document.createElement("span");
                checked_message.setAttribute("slot", "checked-message");
                checked_message.innerHTML = this.model.checked_message;
                fastSwitch.appendChild(checked_message);
                const unchecked_message = document.createElement("span");
                unchecked_message.setAttribute("slot", "unchecked-message");
                unchecked_message.innerHTML = this.model.unchecked_message;
                fastSwitch.appendChild(unchecked_message);
                // const label_el = label({}, checkbox, span({}, labels[i]))
                group.appendChild(fastSwitch);
            }
        }
    }
    exports.FastSwitchGroupView = FastSwitchGroupView;
    FastSwitchGroupView.__name__ = "FastSwitchGroupView";
    class FastSwitchGroup extends checkbox_group_1.CheckboxGroup {
        constructor(attrs) {
            super(attrs);
        }
        static init_FastSwitchGroup() {
            this.prototype.default_view = FastSwitchGroupView;
            this.define(({ Boolean, String }) => ({
                readonly: [Boolean,],
                checked_message: [String,],
                unchecked_message: [String,],
            }));
        }
    }
    exports.FastSwitchGroup = FastSwitchGroup;
    FastSwitchGroup.__name__ = "FastSwitchGroup";
    FastSwitchGroup.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_switch_group";
    FastSwitchGroup.init_FastSwitchGroup();
},
"e9b1cd48b7": /* bokeh_extensions\fast\fast_textarea_input.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const textarea_input_1 = require("@bokehjs/models/widgets/textarea_input");
    const input_widget_1 = require("@bokehjs/models/widgets/input_widget");
    // I tried to inherit from TextAreaInputView but I could not
    // get it working. It created two textareainputs.
    class FastTextAreaInputView extends input_widget_1.InputWidgetView {
        get input_el_any() {
            return this.input_el;
        }
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.name.change, () => { var _a; return this.input_el.name = (_a = this.model.name) !== null && _a !== void 0 ? _a : ""; });
            this.connect(this.model.properties.value.change, () => { this.input_el.value = this.model.value; });
            this.connect(this.model.properties.disabled.change, () => this.input_el.disabled = this.model.disabled);
            this.connect(this.model.properties.placeholder.change, () => this.input_el.placeholder = this.model.placeholder);
            this.connect(this.model.properties.rows.change, () => this.input_el.rows = this.model.rows);
            this.connect(this.model.properties.cols.change, () => this.input_el.cols = this.model.cols);
            this.connect(this.model.properties.max_length.change, () => this.input_el_any.setAttribute("maxlength", this.model.max_length));
            this.connect(this.model.properties.appearance.change, () => this.input_el_any.appearance = this.model.appearance);
            this.connect(this.model.properties.autofocus.change, () => this.input_el_any.autofocus = this.model.autofocus);
            this.connect(this.model.properties.resize.change, () => this.input_el_any.resize = this.model.resize);
            this.connect(this.model.properties.spellcheck.change, () => this.input_el_any.spellcheck = this.model.spellcheck);
            this.connect(this.model.properties.min_length.change, () => this.input_el_any.setAttribute("minlength", this.model.min_length));
            this.connect(this.model.properties.required.change, () => this.input_el_any.required = this.model.required);
            // Could not get readonly working as a property.
            // https://github.com/microsoft/fast/issues/3852
            this.connect(this.model.properties.readonly.change, () => {
                if (this.model.readonly === true) {
                    this.input_el_any.setAttribute("readonly", "");
                }
                else {
                    this.input_el_any.removeAttribute("readonly");
                }
            });
        }
        render() {
            super.render();
            const fastTextArea = document.createElement("fast-text-area");
            this.input_el = fastTextArea;
            this.input_el.className = "bk-fast-input";
            this.input_el.addEventListener("change", () => this.change_input());
            this.group_el.appendChild(this.input_el);
            // For some unknown reason we need to set these properties after the above
            // Otherwise for example the value is reset to ""
            fastTextArea.name = this.model.name;
            fastTextArea.value = this.model.value;
            fastTextArea.disabled = this.model.disabled;
            fastTextArea.placeholder = this.model.placeholder;
            fastTextArea.cols = this.model.cols;
            fastTextArea.rows = this.model.rows;
            if (this.model.max_length != null)
                fastTextArea.setAttribute("maxlength", this.model.max_length);
            fastTextArea.appearance = this.model.appearance;
            fastTextArea.autofocus = this.model.autofocus;
            fastTextArea.resize = this.model.resize;
            fastTextArea.spellcheck = this.model.spellcheck;
            if (this.model.min_length != null)
                fastTextArea.setAttribute("minlength", this.model.min_length);
            fastTextArea.required = this.model.required;
            if (this.model.readonly === true)
                fastTextArea.setAttribute("readonly", "");
        }
        change_input() {
            this.model.value = this.input_el.value;
            super.change_input();
        }
    }
    exports.FastTextAreaInputView = FastTextAreaInputView;
    FastTextAreaInputView.__name__ = "FastTextAreaInputView";
    class FastTextAreaInput extends textarea_input_1.TextAreaInput {
        constructor(attrs) {
            super(attrs);
        }
        static init_FastTextAreaInput() {
            this.prototype.default_view = FastTextAreaInputView;
            this.define(({ Boolean, Number, String }) => ({
                // name inherited
                // value inherited
                // placeholder inherited
                // max_length inherited
                // disabled inherited
                // cols inherited
                // rows inherited
                appearance: [String,],
                autofocus: [Boolean,],
                resize: [String,],
                spellcheck: [Boolean,],
                min_length: [Number,],
                required: [Boolean,],
                readonly: [Boolean,],
            }));
        }
    }
    exports.FastTextAreaInput = FastTextAreaInput;
    FastTextAreaInput.__name__ = "FastTextAreaInput";
    FastTextAreaInput.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_textarea_input";
    FastTextAreaInput.init_FastTextAreaInput();
},
"92a4b5b2b8": /* bokeh_extensions\fast\fast_text_input.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const text_input_1 = require("@bokehjs/models/widgets/text_input");
    const input_widget_1 = require("@bokehjs/models/widgets/input_widget");
    // I tried to inherit from TextInputView but I could not
    // get it working. It created two textinputs.
    class FastTextInputView extends input_widget_1.InputWidgetView {
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.name.change, () => { var _a; return this.input_el.name = (_a = this.model.name) !== null && _a !== void 0 ? _a : ""; });
            this.connect(this.model.properties.value.change, () => { this.input_el.value = this.model.value; console.log("value"); });
            this.connect(this.model.properties.value_input.change, () => this.input_el.value = this.model.value_input);
            this.connect(this.model.properties.disabled.change, () => this.input_el.disabled = this.model.disabled);
            this.connect(this.model.properties.placeholder.change, () => this.input_el.placeholder = this.model.placeholder);
            this.connect(this.model.properties.appearance.change, () => this.input_el_any.appearance = this.model.appearance);
            this.connect(this.model.properties.autofocus.change, () => this.input_el_any.autofocus = this.model.autofocus);
            this.connect(this.model.properties.type_of_text.change, () => this.input_el_any.type = this.model.type_of_text);
            this.connect(this.model.properties.max_length.change, () => this.input_el_any.setAttribute("maxlength", this.model.max_length));
            this.connect(this.model.properties.min_length.change, () => this.input_el_any.setAttribute("minlength", this.model.min_length));
            this.connect(this.model.properties.pattern.change, () => this.input_el_any.pattern = this.model.pattern);
            // Could not get size working. It raises an error
            // this.connect(this.model.properties.size.change, () => this.input_el_any.size = this.model.size)
            this.connect(this.model.properties.spellcheck.change, () => this.input_el_any.spellcheck = this.model.spellcheck);
            this.connect(this.model.properties.required.change, () => this.input_el_any.required = this.model.required);
            // Could not get readonly working as a property.
            // https://github.com/microsoft/fast/issues/3852
            this.connect(this.model.properties.readonly.change, () => this.input_el_any.setAttribute("readonly", this.model.readonly));
        }
        get input_el_any() {
            return this.input_el;
        }
        render() {
            super.render();
            const fastTextField = document.createElement("fast-text-field");
            this.input_el = fastTextField;
            this.input_el.className = "bk-fast-input";
            this.input_el.addEventListener("change", () => this.change_input());
            this.input_el.addEventListener("input", () => this.change_input_oninput());
            this.group_el.appendChild(this.input_el);
            // For some unknown reason we need to set these properties after the above
            // Otherwise for example the value is reset to ""
            fastTextField.name = this.model.name;
            fastTextField.value = this.model.value;
            fastTextField.appearance = this.model.appearance;
            fastTextField.autofocus = this.model.autofocus;
            fastTextField.placeholder = this.model.placeholder;
            fastTextField.disabled = this.model.disabled;
            fastTextField.type = this.model.type_of_text;
            fastTextField.setAttribute("maxlength", this.model.max_length);
            fastTextField.setAttribute("minlength", this.model.min_length);
            fastTextField.pattern = this.model.pattern;
            // Could not get size working. It raises an error.
            // fastTextField.size = this.model.size;
            fastTextField.spellcheck = this.model.spellcheck;
            fastTextField.required = this.model.required;
            fastTextField.disabled = this.model.disabled;
            fastTextField.setAttribute("readonly", this.model.readonly);
        }
        change_input() {
            this.model.value = this.input_el.value;
            super.change_input();
        }
        change_input_oninput() {
            this.model.value_input = this.input_el.value;
            super.change_input();
        }
    }
    exports.FastTextInputView = FastTextInputView;
    FastTextInputView.__name__ = "FastTextInputView";
    class FastTextInput extends text_input_1.TextInput {
        constructor(attrs) {
            super(attrs);
        }
        static init_FastTextInput() {
            this.prototype.default_view = FastTextInputView;
            this.define(({ Any, Boolean, Number, String }) => ({
                // name inherited
                // value inherited
                appearance: [String,],
                autofocus: [Boolean,],
                // placeholder inherited
                type_of_text: [String,],
                // max_length: [Number, ],
                min_length: [Number,],
                pattern: [String,],
                size: [Any,],
                spellcheck: [Boolean,],
                required: [Boolean,],
                // disabled inherited
                readonly: [Boolean, false],
            }));
        }
    }
    exports.FastTextInput = FastTextInput;
    FastTextInput.__name__ = "FastTextInput";
    FastTextInput.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_text_input";
    FastTextInput.init_FastTextInput();
},
"eb2d75c5b0": /* bokeh_extensions\pivot_table.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    // Bokeh model for perspective-viewer
    // See https://github.com/finos/perspective/tree/master/packages/perspective-viewer
    // See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const dom_1 = require("@bokehjs/core/dom");
    const shared_1 = require("88538263fa") /* ./shared */;
    // The view of the Bokeh extension/ HTML element
    // Here you can define how to render the model as well as react to model changes or View events.
    class PivotTableView extends html_box_1.HTMLBoxView {
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.source.properties.data.change, this.setData);
        }
        render() {
            super.render();
            this.container = dom_1.div({ class: "pnx-pivot-table" });
            shared_1.set_size(this.container, this.model);
            this.el.appendChild(this.container);
            this.setData();
        }
        setData() {
            console.log("setData");
            console.log(this.model.source.data);
            let data = shared_1.transform_cds_to_records(this.model.source);
            this.pivot_table_element = $(this.container);
            console.log(data);
            this.pivot_table_element.pivotUI(data, {});
        }
    }
    exports.PivotTableView = PivotTableView;
    PivotTableView.__name__ = "PivotTableView";
    // The Bokeh .ts model corresponding to the Bokeh .py model
    class PivotTable extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_PivotTable() {
            this.prototype.default_view = PivotTableView;
            this.define(({ Any }) => ({
                source: [Any,],
                source_stream: [Any,],
                source_patch: [Any,],
            }));
        }
    }
    exports.PivotTable = PivotTable;
    PivotTable.__name__ = "PivotTable";
    PivotTable.__module__ = "awesome_panel_extensions.bokeh_extensions.pivot_table";
    PivotTable.init_PivotTable();
},
"88538263fa": /* bokeh_extensions\shared.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    /** Function copied from the panel\models\layout.ts file of Panel
     * It is used for some models like deckgl, progress and vtlklayout
     * I have not yet understood why
     * @param el
     * @param model
     */
    function set_size(el, model) {
        let width_policy = model.width != null ? "fixed" : "fit";
        let height_policy = model.height != null ? "fixed" : "fit";
        const { sizing_mode } = model;
        if (sizing_mode != null) {
            if (sizing_mode == "fixed")
                width_policy = height_policy = "fixed";
            else if (sizing_mode == "stretch_both")
                width_policy = height_policy = "max";
            else if (sizing_mode == "stretch_width")
                width_policy = "max";
            else if (sizing_mode == "stretch_height")
                height_policy = "max";
            else {
                switch (sizing_mode) {
                    case "scale_width":
                        width_policy = "max";
                        height_policy = "min";
                        break;
                    case "scale_height":
                        width_policy = "min";
                        height_policy = "max";
                        break;
                    case "scale_both":
                        width_policy = "max";
                        height_policy = "max";
                        break;
                    default:
                        throw new Error("unreachable");
                }
            }
        }
        if (width_policy == "fixed" && model.width)
            el.style.width = model.width + "px";
        else if (width_policy == "max")
            el.style.width = "100%";
        if (height_policy == "fixed" && model.height)
            el.style.height = model.height + "px";
        else if (height_policy == "max")
            el.style.height = "100%";
    }
    exports.set_size = set_size;
    /** Transform the data of the cds to 'records' format, i.e. a list of objects
     *
     *  For example transforms to [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
     *
     *  Some js libraries like perspective-viewer uses this format to load data.
     *
     * @param cds
     */
    function transform_cds_to_records(cds) {
        const data = [];
        const columns = cds.columns();
        const cdsLength = cds.get_length();
        if (columns.length === 0 || cdsLength === null) {
            return [];
        }
        for (let i = 0; i < cdsLength; i++) {
            const item = {};
            for (const column of columns) {
                let array = cds.get_array(column);
                const shape = array[0].shape == null ? null : array[0].shape;
                if ((shape != null) && (shape.length > 1) && (typeof shape[0] == "number"))
                    item[column] = array.slice(i * shape[1], i * shape[1] + shape[1]);
                else
                    item[column] = array[i];
            }
            data.push(item);
        }
        return data;
    }
    exports.transform_cds_to_records = transform_cds_to_records;
    /** Helper function used to incrementally build a html element string
     *
     *  For example toAttribute("columns", ['x','y']) returns ' columns="['x','y']"
     *  For example toAttribute("columns", null) returns ""
     *
     * @param attribute
     * @param value
     */
    function toAttribute(attribute, value) {
        if (value === null) {
            return "";
        }
        if (typeof value !== "string") {
            value = JSON.stringify(value);
        }
        return " " + attribute + "='" + value + "'";
    }
    exports.toAttribute = toAttribute;
},
"5f262d0d3a": /* bokeh_extensions\icon.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const abstract_icon_1 = require("@bokehjs/models/widgets/abstract_icon");
    // See https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
    /**
     * @param {String} HTML representing a single element
     * @return {Element}
     */
    function htmlToElement(html) {
        var template = document.createElement('template');
        html = html.trim(); // Never return a text node of whitespace as the result
        template.innerHTML = html;
        return template.content.firstChild;
    }
    class IconView extends abstract_icon_1.AbstractIconView {
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.change, () => this.render());
        }
        render() {
            super.render();
            if (this.model.text === null && this.model.text === "") {
                return;
            }
            this.el.innerHTML = "";
            const iconEl = htmlToElement(this.model.text);
            this.el.appendChild(iconEl);
            this.el.style.display = "inline";
            this.el.style.height = `${this.model.size}em`;
            this.el.style.width = `${this.model.size}em`;
            iconEl.style.verticalAlign = "middle";
            iconEl.style.height = `${this.model.size}em`;
            iconEl.style.width = `${this.model.size}em`;
            iconEl.style.fill = this.model.fill_color;
            if (this.model.spin_duration > 0) {
                // See https://codepen.io/eveness/pen/BjLaoa
                const animationDuration = `${this.model.spin_duration}ms`;
                iconEl.style.setProperty("-webkit-animation-name", "spin");
                iconEl.style.setProperty("-webkit-animation-duration", animationDuration);
                iconEl.style.setProperty("-webkit-animation-iteration-count", "infinite");
                iconEl.style.setProperty("-webkit-animation-timing-function", "linear");
                iconEl.style.setProperty("-moz-animation-name", "spin");
                iconEl.style.setProperty("-moz-animation-duration", animationDuration);
                iconEl.style.setProperty("-moz-animation-iteration-count", "infinite");
                iconEl.style.setProperty("-moz-animation-timing-function", "linear");
                iconEl.style.setProperty("-ms-animation-name", "spin");
                iconEl.style.setProperty("-ms-animation-duration", animationDuration);
                iconEl.style.setProperty("-ms-animation-iteration-count", "infinite");
                iconEl.style.setProperty("-ms-animation-timing-function", "linear");
                iconEl.style.setProperty("animation-name", "spin");
                iconEl.style.setProperty("animation-duration", animationDuration);
                iconEl.style.setProperty("animation-iteration-count", "infinite");
                iconEl.style.setProperty("animation-timing-function", "linear");
            }
            iconEl.classList.add("icon");
            if (this.model.label != null && this.model.label !== "") {
                const label = this.model.label.toLowerCase().replace(" ", "");
                iconEl.classList.add(`icon-${label}`);
            }
        }
    }
    exports.IconView = IconView;
    IconView.__name__ = "IconView";
    class Icon extends abstract_icon_1.AbstractIcon {
        constructor(attrs) {
            super(attrs);
        }
        static init_Icon() {
            this.prototype.default_view = IconView;
            this.define(({ String, Number, Int }) => ({
                label: [String,],
                text: [String,],
                size: [Number, 1.0],
                fill_color: [String, "currentColor"],
                spin_duration: [Int, 0],
            }));
        }
    }
    exports.Icon = Icon;
    Icon.__name__ = "Icon";
    Icon.__module__ = "awesome_panel_extensions.bokeh_extensions.icon";
    Icon.init_Icon();
},
"514b75040d": /* bokeh_extensions\web_component.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const dom_1 = require("@bokehjs/core/dom");
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const inputs = tslib_1.__importStar(require("@bokehjs/styles/widgets/inputs.css"));
    function htmlDecode(input) {
        var doc = new DOMParser().parseFromString(input, "text/html");
        return doc.documentElement.textContent;
    }
    class WebComponentView extends html_box_1.HTMLBoxView {
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.name.change, () => this.handleNameChange());
            this.connect(this.model.properties.innerHTML.change, () => this.render());
            this.connect(this.model.properties.attributesLastChange.change, () => this.handleAttributesLastChangeChange());
            this.connect(this.model.properties.propertiesLastChange.change, () => this.handlePropertiesLastChangeChange());
            this.connect(this.model.properties.columnDataSource.change, () => this.handleColumnDataSourceChange());
        }
        handleNameChange() {
            if (this.label_el)
                this.label_el.textContent = this.model.name;
        }
        render() {
            super.render();
            if (this.el.innerHTML !== this.model.innerHTML)
                this.createOrUpdateWebComponentElement();
        }
        after_layout() {
            if ("after_layout" in this.webComponentElement)
                this.webComponentElement.after_layout();
        }
        createOrUpdateWebComponentElement() {
            if (this.webComponentElement)
                this.webComponentElement.onchange = null;
            // @Philippfr: How do we make sure the component is automatically sized according to the
            // parameters of the WebComponent like width, height, sizing_mode etc?
            // Should we set height and width to 100% or similar?
            // For now I've set min_height as a part of .py __init__ for some of the Wired components?
            const title = this.model.name;
            if (this.model.componentType === "inputgroup" && title) {
                this.group_el = dom_1.div({ class: inputs.input_group }, this.label_el);
                this.group_el.innerHTML = htmlDecode(this.model.innerHTML);
                this.webComponentElement = this.group_el.firstElementChild;
                this.label_el = dom_1.label({ style: { display: title.length == 0 ? "none" : "" } }, title);
                this.group_el.insertBefore(this.label_el, this.webComponentElement);
                this.el.appendChild(this.group_el);
            }
            else {
                this.el.innerHTML = htmlDecode(this.model.innerHTML);
                this.webComponentElement = this.el.firstElementChild;
            }
            this.activate_scripts(this.webComponentElement.parentNode);
            // Initialize properties
            this.initPropertyValues();
            this.handlePropertiesLastChangeChange();
            this.handleColumnDataSourceChange();
            // Subscribe to events
            this.webComponentElement.onchange = (ev) => this.handlePropertiesChange(ev);
            this.addEventListeners();
            this.addAttributesMutationObserver();
        }
        addAttributesMutationObserver() {
            if (!this.model.attributesToWatch)
                return;
            let options = {
                childList: false,
                attributes: true,
                characterData: false,
                subtree: false,
                attributeFilter: Object.keys(this.model.attributesToWatch),
                attributeOldValue: false,
                characterDataOldValue: false
            };
            const handleAttributesChange = (_) => {
                let attributesLastChange = new Object();
                for (let attribute in this.model.attributesToWatch) {
                    const value = this.webComponentElement.getAttribute(attribute);
                    attributesLastChange[attribute] = value;
                }
                if (this.model.attributesLastChange !== attributesLastChange)
                    this.model.attributesLastChange = attributesLastChange;
            };
            let observer = new MutationObserver(handleAttributesChange);
            observer.observe(this.webComponentElement, options);
        }
        addEventListeners() {
            this.eventsCount = {};
            for (let event in this.model.eventsToWatch) {
                this.eventsCount[event] = 0;
                this.webComponentElement.addEventListener(event, (ev) => this.eventHandler(ev), false);
            }
        }
        transform_cds_to_records(cds) {
            const data = [];
            const columns = cds.columns();
            const cdsLength = cds.get_length();
            if (columns.length === 0 || cdsLength === null) {
                return [];
            }
            for (let i = 0; i < cdsLength; i++) {
                const item = {};
                for (const column of columns) {
                    let array = cds.get_array(column);
                    const shape = array[0].shape == null ? null : array[0].shape;
                    if ((shape != null) && (shape.length > 1) && (typeof shape[0] == "number"))
                        item[column] = array.slice(i * shape[1], i * shape[1] + shape[1]);
                    else
                        item[column] = array[i];
                }
                data.push(item);
            }
            return data;
        }
        // https://stackoverflow.com/questions/5999998/check-if-a-variable-is-of-function-type
        isFunction(functionToCheck) {
            if (functionToCheck) {
                const stringName = {}.toString.call(functionToCheck);
                return stringName === '[object Function]' || stringName === '[object AsyncFunction]';
            }
            else {
                return false;
            }
        }
        /**
         * Handles changes to `this.model.columnDataSource`
         * by
         * updating the data source of `this.webComponentElement`
         * using the function or property specifed in `this.model.columnDataSourceLoadFunction`
         */
        handleColumnDataSourceChange() {
            // @Philippfr: Right now we just reload all the data
            // For example Perspective has an `update` function to append data
            // Is this something we could/ should support?
            if (this.model.columnDataSource) {
                let data; // list
                const columnDataSourceOrient = this.model.columnDataSourceOrient;
                if (columnDataSourceOrient === "records")
                    data = this.transform_cds_to_records(this.model.columnDataSource);
                else
                    data = this.model.columnDataSource.data; // @ts-ignore
                if (this.model.columnDataSourceLoadFunction === null) {
                    return;
                }
                const loadFunctionName = this.model.columnDataSourceLoadFunction.toString();
                const loadFunction = this.webComponentElement[loadFunctionName];
                if (this.isFunction(loadFunction))
                    this.webComponentElement[loadFunctionName](data);
                else
                    this.webComponentElement[loadFunctionName] = data;
            }
            // Todo: handle situation where this.model.columnDataSource is null
        }
        activate_scripts(el) {
            Array.from(el.querySelectorAll("script")).forEach((oldScript) => {
                const newScript = document.createElement("script");
                Array.from(oldScript.attributes)
                    .forEach(attr => newScript.setAttribute(attr.name, attr.value));
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                if (oldScript.parentNode)
                    oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        }
        // See https://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key
        /**
         * Example:
         *
         * `get_nested_property(element, "textInput.value")` returns `element.textInput.value`
         *
         * @param element
         * @param property_
         */
        get_nested_property(element, property_) {
            property_ = property_.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
            property_ = property_.replace(/^\./, ''); // strip a leading dot
            let a = property_.split('.');
            for (let i = 0, n = a.length; i < n; ++i) {
                let k = a[i];
                if (k in element)
                    element = element[k];
                else
                    return "";
            }
            return element;
        }
        set_nested_property(element, property_, value) {
            // @Phillipfr: I need your help to understand and solve this
            // hack: Setting the value of the WIRED-SLIDER before its ready
            // will destroy the setter.
            // I don't yet understand this.
            // if (["WIRED-SLIDER"].indexOf(element.tagName)>=0){
            //   const setter = element.__lookupSetter__(property_);
            //   if (!setter){return}
            // }
            const pList = property_.split('.');
            if (pList.length === 1)
                element[property_] = value;
            else {
                const len = pList.length;
                for (let i = 0; i < len - 1; i++) {
                    const elem = pList[i];
                    if (!element[elem])
                        element[elem] = {};
                    element = element[elem];
                }
                element[pList[len - 1]] = value;
            }
        }
        /**
         * Handles events from `eventsToWatch` by
         *
         * - Incrementing the count of the event
         * - Checking if any properties have changed
         *
         * @param ev The Event Fired
         */
        eventHandler(ev) {
            let event = ev.type;
            this.eventsCount[event] += 1;
            let eventsCountLastChanged = {};
            eventsCountLastChanged[event] = this.eventsCount[event];
            this.model.eventsCountLastChange = eventsCountLastChanged;
            this.checkIfPropertiesChanged();
        }
        /** Checks if any properties have changed. In case this is communicated to the server.
         *
         * For example the Wired `DropDown` does not run the `onchange` event handler when the selection changes.
         * Insted the `select` event is fired. Thus we can subscribe to this event and manually check for property changes.
         */
        checkIfPropertiesChanged() {
            const propertiesChange = {};
            for (const property in this.model.propertiesToWatch) {
                const oldValue = this.propertyValues[property];
                const newValue = this.get_nested_property(this.webComponentElement, property);
                if (oldValue != newValue) {
                    propertiesChange[property] = newValue;
                    this.propertyValues[property] = newValue;
                }
            }
            if (Object.keys(propertiesChange).length)
                this.model.propertiesLastChange = propertiesChange;
        }
        /** Handles the `WebComponentElement` `(on)change` event
         *
         * Communicates any changed properties in `propertiesToWatch` to the server
         * by updating `this.model.propertiesLastChange`.
         * @param ev
         */
        handlePropertiesChange(ev) {
            const properties_change = new Object();
            for (const property in this.model.propertiesToWatch) {
                if (ev.detail && property in ev.detail) {
                    properties_change[property] = ev.detail[property];
                    this.propertyValues[property] = ev.detail[property];
                }
                else if (ev.target && property in ev.target) {
                    properties_change[property] = ev.target[property];
                    this.propertyValues[property] = ev.target[property];
                }
            }
            if (Object.keys(properties_change).length)
                this.model.propertiesLastChange = properties_change;
        }
        initPropertyValues() {
            this.propertyValues = new Object();
            if (!this.webComponentElement) {
                return;
            }
            for (let property in this.model.propertiesToWatch) {
                let old_value = this.propertyValues[property];
                let new_value = this.get_nested_property(this.webComponentElement, property);
                if (new_value !== old_value) {
                    this.propertyValues[property] = new_value;
                }
            }
        }
        /**
         * Handles changes to `this.model.attributesLastChange`
         * by
         * updating the attributes of `this.webComponentElement` accordingly
         */
        handleAttributesLastChangeChange() {
            if (!this.webComponentElement)
                return;
            let attributesLastChange = this.model.attributesLastChange;
            for (let attribute in this.model.attributesLastChange) {
                if (attribute in this.model.attributesToWatch) {
                    let old_value = this.webComponentElement.getAttribute(attribute);
                    let new_value = attributesLastChange[attribute];
                    if (old_value !== new_value) {
                        if (new_value === null)
                            this.webComponentElement.removeAttribute(attribute);
                        else
                            this.webComponentElement.setAttribute(attribute, new_value);
                    }
                }
            }
        }
        /**
        * Handles changes to `this.model.propertiesLastChange`
        * by
        * updating the properties of `this.webComponentElement` accordingly
        */
        handlePropertiesLastChangeChange() {
            if (!this.webComponentElement) {
                return;
            }
            let propertiesLastChange = this.model.propertiesLastChange;
            for (let property in this.model.propertiesLastChange) {
                if (property in this.model.propertiesToWatch) {
                    let value = propertiesLastChange[property];
                    this.set_nested_property(this.webComponentElement, property, value);
                }
            }
        }
    }
    exports.WebComponentView = WebComponentView;
    WebComponentView.__name__ = "WebComponentView";
    class WebComponent extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_WebComponent() {
            this.prototype.default_view = WebComponentView;
            this.define(({ Any, String }) => ({
                componentType: [String, 'htmlbox'],
                innerHTML: [String, ''],
                attributesToWatch: [Any],
                attributesLastChange: [Any],
                propertiesToWatch: [Any],
                propertiesLastChange: [Any],
                eventsToWatch: [Any],
                eventsCountLastChange: [Any],
                columnDataSource: [Any],
                columnDataSourceOrient: [Any],
                columnDataSourceLoadFunction: [Any],
            }));
        }
    }
    exports.WebComponent = WebComponent;
    WebComponent.__name__ = "WebComponent";
    WebComponent.__module__ = "awesome_panel_extensions.bokeh_extensions.web_component";
    WebComponent.init_WebComponent();
},
}, "ed583be1cf", {"index":"ed583be1cf","bokeh_extensions/index":"ea89eb96d7","bokeh_extensions/fast/fast_anchor":"3ab92f5894","bokeh_extensions/fast/fast_button":"1d9a6373ec","bokeh_extensions/fast/fast_checkbox_group":"b62557482c","bokeh_extensions/fast/fast_switch_group":"b714a2453d","bokeh_extensions/fast/fast_textarea_input":"e9b1cd48b7","bokeh_extensions/fast/fast_text_input":"92a4b5b2b8","bokeh_extensions/pivot_table":"eb2d75c5b0","bokeh_extensions/shared":"88538263fa","bokeh_extensions/icon":"5f262d0d3a","bokeh_extensions/web_component":"514b75040d"}, {});});
//# sourceMappingURL=awesome_panel_extensions.js.map
