import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
const win = window;
export class FastStylerView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.provider.change, () => { this.setProvider(), this.getProperties(); });
        this.connect(this.model.properties.background_color.change, () => { this.setBackgroundColor(); this.getProperties(); console.log("background_color"); });
        this.connect(this.model.properties.neutral_color.change, () => { this.setNeutralColor(); this.getProperties(); console.log("neutral_color"); });
        this.connect(this.model.properties.accent_base_color.change, () => { this.setAccentColor(); this.getProperties(); console.log("background_color"); });
        this.connect(this.model.properties.corner_radius.change, () => { this.provider.cornerRadius = this.model.corner_radius; console.log("corner_radius"); });
        this.connect(this.model.properties.body_font.change, () => { this.setBodyFont(); this.getProperties(); console.log("body_font"); });
    }
    render() {
        super.render();
        this.el.style.display = "hide";
        this.setProvider();
        this.setBackgroundColor();
        this.setAccentColor();
        this.setNeutralColor();
        this.getProperties();
    }
    setProvider() {
        console.log("set provider");
        console.log(this.model.provider);
        this.provider = document.getElementById(this.model.provider);
        console.log(this.provider);
    }
    setBackgroundColor() {
        if (this.model.background_color) {
            this.provider.setAttribute("background-color", this.model.background_color);
        }
    }
    setAccentColor() {
        if (this.model.accent_base_color) {
            win.setAccentColor(this.model.accent_base_color, "#" + this.model.provider);
        }
    }
    setNeutralColor() {
        if (this.model.neutral_color) {
            console.log(this.model.neutral_color);
            win.setNeutralColor(this.model.neutral_color, "#" + this.model.provider);
            console.log("neutralColor set");
        }
    }
    setBodyFont() {
        document.getElementsByTagName("body")[0].style.setProperty("--body-font", this.model.body_font);
    }
    getProperties() {
        console.log("getProperties");
        const model = this.model;
        const provider = this.provider;
        console.log(provider.backgroundColor, model.background_color);
        if (provider.backgroundColor && model.background_color !== provider.backgroundColor) {
            model.background_color = provider.backgroundColor;
            console.log("set background");
        }
        if (provider.accentBaseColor && model.accent_base_color !== provider.accentBaseColor) {
            model.accent_base_color = provider.accentBaseColor;
        }
        let palette = provider.accentPalette;
        let index = palette.indexOf(this.provider.accentBaseColor.toUpperCase());
        if (provider.accentFillActiveDelta !== undefined) {
            model.accent_fill_active = palette[index + provider.accentFillActiveDelta];
        }
        if (provider.accentFillHoverDelta !== undefined) {
            model.accent_fill_hover = palette[index + provider.accentFillHoverDelta];
        }
        if (provider.accentFillRestDelta !== undefined) {
            model.accent_fill_rest = palette[index + provider.accentFillRestDelta];
        }
        if (provider.accentForegroundActiveDelta !== undefined) {
            model.accent_foreground_active = palette[index + provider.accentForegroundActiveDelta];
        }
        if (provider.accentForegroundCutDelta !== undefined) {
            model.accent_foreground_cut_rest = palette[index + provider.accentForegroundCutDelta];
        }
        if (provider.accentForegroundHoverDelta !== undefined) {
            model.accent_foreground_hover = palette[index + provider.accentForegroundHoverDelta];
        }
        if (provider.accentForegroundRestDelta !== undefined) {
            model.accent_foreground_rest = palette[index + provider.accentForegroundRestDelta];
        }
        let value;
        value = window.getComputedStyle(provider).getPropertyValue('--body-font').trim();
        if (value !== "") {
            model.body_font = value;
        }
        value = window.getComputedStyle(provider).getPropertyValue('--accent-foreground-cut-rest').trim();
        if (value !== "") {
            model.accent_foreground_cut_rest = value;
        }
        value = window.getComputedStyle(provider).getPropertyValue('--neutral-outline-active').trim();
        if (value !== "") {
            model.neutral_outline_active = value;
        }
        value = window.getComputedStyle(provider).getPropertyValue('--neutral-outline-hover').trim();
        if (value !== "") {
            model.neutral_outline_hover = value;
        }
        value = window.getComputedStyle(provider).getPropertyValue('--neutral-outline-rest').trim();
        if (value !== "") {
            model.neutral_outline_rest = value;
        }
        value = window.getComputedStyle(provider).getPropertyValue('--neutral-focus').trim();
        if (value !== "") {
            model.neutral_focus = value;
        }
        console.log("neutral_focus", value, model.neutral_focus);
        value = window.getComputedStyle(provider).getPropertyValue('--neutral-foreground-rest').trim();
        if (value !== "") {
            model.neutral_foreground_rest = value;
        }
        console.log("--neutral-foreground-rest", value, model.neutral_foreground_rest);
        this.model.updates += 1;
    }
}
FastStylerView.__name__ = "FastStylerView";
// The Bokeh .ts model corresponding to the Bokeh .py model
export class FastStyler extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_FastStyler() {
        this.prototype.default_view = FastStylerView;
        this.define({
            provider: [p.String,],
            background_color: [p.String,],
            neutral_color: [p.String,],
            accent_base_color: [p.String,],
            corner_radius: [p.Int,],
            body_font: [p.String,],
            accent_fill_active: [p.String,],
            accent_fill_hover: [p.String,],
            accent_fill_rest: [p.String,],
            accent_foreground_active: [p.String,],
            accent_foreground_cut_rest: [p.String,],
            accent_foreground_hover: [p.String,],
            accent_foreground_rest: [p.String,],
            neutral_outline_active: [p.String,],
            neutral_outline_hover: [p.String,],
            neutral_outline_rest: [p.String,],
            neutral_focus: [p.String,],
            neutral_foreground_rest: [p.String,],
            updates: [p.Int, 0],
        });
    }
}
FastStyler.__name__ = "FastStyler";
FastStyler.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_styler";
FastStyler.init_FastStyler();
//# sourceMappingURL=fast_styler.js.map