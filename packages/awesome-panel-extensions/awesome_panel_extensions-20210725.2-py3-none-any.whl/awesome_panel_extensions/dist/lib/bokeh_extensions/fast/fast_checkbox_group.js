import { CheckboxGroup, CheckboxGroupView } from "@bokehjs/models/widgets/checkbox_group";
import * as inputs from "@bokehjs/styles/widgets/inputs.css";
import { div } from "@bokehjs/core/dom";
import { includes } from "@bokehjs/core/util/array";
// Browse the fast-button api here  https://explore.fast.design/components/fast-button
export class FastCheckboxGroupView extends CheckboxGroupView {
    render() {
        // Cannot call super.render() as this will add the group twice
        // super.render()
        const group = div({ class: [inputs.input_group, this.model.inline ? inputs.inline : null] });
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
            if (includes(active, i))
                checkbox.checked = true;
            // const label_el = label({}, checkbox, span({}, labels[i]))
            group.appendChild(checkbox);
        }
    }
}
FastCheckboxGroupView.__name__ = "FastCheckboxGroupView";
export class FastCheckboxGroup extends CheckboxGroup {
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
FastCheckboxGroup.__name__ = "FastCheckboxGroup";
FastCheckboxGroup.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_checkbox_group";
FastCheckboxGroup.init_FastCheckboxGroup();
//# sourceMappingURL=fast_checkbox_group.js.map