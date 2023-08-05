import { HTMLBox, HTMLBoxView } from "../layouts/html_box";
export class WidgetView extends HTMLBoxView {
    get orientation() {
        return "horizontal";
    }
    get default_size() {
        return this.model.default_size;
    }
    _width_policy() {
        return this.orientation == "horizontal" ? super._width_policy() : "fixed";
    }
    _height_policy() {
        return this.orientation == "horizontal" ? "fixed" : super._height_policy();
    }
    box_sizing() {
        const sizing = super.box_sizing();
        if (this.orientation == "horizontal") {
            if (sizing.width == null)
                sizing.width = this.default_size;
        }
        else {
            if (sizing.height == null)
                sizing.height = this.default_size;
        }
        return sizing;
    }
}
WidgetView.__name__ = "WidgetView";
export class Widget extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_Widget() {
        this.define(({ Number }) => ({
            default_size: [Number, 300],
        }));
        this.override({
            margin: [5, 5, 5, 5],
        });
    }
}
Widget.__name__ = "Widget";
Widget.init_Widget();
//# sourceMappingURL=widget.js.map