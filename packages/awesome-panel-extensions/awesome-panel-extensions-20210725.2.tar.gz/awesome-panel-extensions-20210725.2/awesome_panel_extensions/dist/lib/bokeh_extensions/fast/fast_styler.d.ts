import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export declare class FastStylerView extends HTMLBoxView {
    model: FastStyler;
    provider: any;
    connect_signals(): void;
    render(): void;
    setProvider(): void;
    setBackgroundColor(): void;
    setAccentColor(): void;
    setNeutralColor(): void;
    setBodyFont(): void;
    getProperties(): void;
}
export declare namespace FastStyler {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        provider: p.Property<string>;
        background_color: p.Property<string>;
        neutral_color: p.Property<string>;
        accent_base_color: p.Property<string>;
        corner_radius: p.Property<number>;
        body_font: p.Property<string>;
        accent_fill_active: p.Property<string>;
        accent_fill_hover: p.Property<string>;
        accent_fill_rest: p.Property<string>;
        accent_foreground_active: p.Property<string>;
        accent_foreground_cut_rest: p.Property<string>;
        accent_foreground_hover: p.Property<string>;
        accent_foreground_rest: p.Property<string>;
        neutral_outline_active: p.Property<string>;
        neutral_outline_hover: p.Property<string>;
        neutral_outline_rest: p.Property<string>;
        neutral_focus: p.Property<string>;
        neutral_foreground_rest: p.Property<string>;
        updates: p.Property<number>;
    };
}
export interface FastStyler extends FastStyler.Attrs {
}
export declare class FastStyler extends HTMLBox {
    properties: FastStyler.Props;
    constructor(attrs?: Partial<FastStyler.Attrs>);
    static __module__: string;
    static init_FastStyler(): void;
}
