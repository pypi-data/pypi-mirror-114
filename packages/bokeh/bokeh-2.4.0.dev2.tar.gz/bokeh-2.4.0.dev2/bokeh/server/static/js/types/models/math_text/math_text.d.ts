import * as p from "../../core/properties";
import * as visuals from "../../core/visuals";
import { Context2d } from "../../core/util/canvas";
import { Model } from "../../model";
import { Size } from "../../core/types";
import { View } from "../../core/view";
import { RendererView } from "../renderers/renderer";
declare type Position = {
    sx: number;
    sy: number;
    x_anchor?: number | "left" | "center" | "right";
    y_anchor?: number | "top" | "center" | "baseline" | "bottom";
};
/**
 * Helper class to rendering MathText into Canvas
 */
export declare class MathTextView extends View {
    model: MathText;
    parent: RendererView;
    angle?: number;
    position: Position;
    has_image_loaded: boolean;
    align: "left" | "center" | "right" | "justify";
    private _base_font_size;
    set base_font_size(v: number | null | undefined);
    private font_size_scale;
    private font;
    private color;
    private svg_image;
    private svg_element;
    lazy_initialize(): Promise<void>;
    set visuals(v: visuals.Text);
    /**
     * Calculates position of element after considering
     * anchor and dimensions
     */
    protected _computed_position(): {
        x: number;
        y: number;
    };
    /**
     * Uses the width, height and given angle to calculate the size
    */
    size(): Size;
    private get_text_dimensions;
    private get_image_dimensions;
    private get_dimensions;
    private load_math_jax_script;
    private get_math_jax;
    /**
     * Render text into a SVG with MathJax and load it into memory.
     */
    private load_image;
    /**
     * Takes a Canvas' Context2d and if the image has already
     * been loaded draws the image in it otherwise draws the model's text.
    */
    paint(ctx: Context2d): void;
}
export declare namespace MathText {
    type Attrs = p.AttrsOf<Props>;
    type Props = Model.Props & {
        text: p.Property<string>;
    };
}
export interface MathText extends MathText.Attrs {
}
export declare class MathText extends Model {
    properties: MathText.Props;
    __view_type__: MathTextView;
    constructor(attrs?: Partial<MathText.Attrs>);
    static init_MathText(): void;
}
export {};
//# sourceMappingURL=math_text.d.ts.map