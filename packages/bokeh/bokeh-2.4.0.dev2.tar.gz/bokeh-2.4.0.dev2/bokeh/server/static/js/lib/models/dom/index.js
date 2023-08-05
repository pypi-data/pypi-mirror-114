import { Model } from "../../model";
import { LayoutDOM } from "../layouts/layout_dom";
import { Styles } from "./styles";
import { span } from "../../core/dom";
import { View } from "../../core/view";
import { DOMView } from "../../core/dom_view";
import { build_views, remove_views } from "../../core/build_views";
import { isString } from "../../core/util/types";
import { entries } from "../../core/util/object";
import * as styles from "../../styles/tooltips.css";
import { _get_column_value } from "../../core/util/templating";
export { Styles };
export class DOMNodeView extends DOMView {
}
DOMNodeView.__name__ = "DOMNodeView";
export class DOMNode extends Model {
    constructor(attrs) {
        super(attrs);
    }
    static init_DOMNode() { }
}
DOMNode.__name__ = "DOMNode";
DOMNode.__module__ = "bokeh.models.dom";
DOMNode.init_DOMNode();
export class TextView extends DOMNodeView {
    render() {
        super.render();
        this.el.textContent = this.model.content;
    }
    _createElement() {
        return document.createTextNode("");
    }
}
TextView.__name__ = "TextView";
export class Text extends DOMNode {
    constructor(attrs) {
        super(attrs);
    }
    static init_Text() {
        this.prototype.default_view = TextView;
        this.define(({ String }) => ({
            content: [String, ""],
        }));
    }
}
Text.__name__ = "Text";
Text.init_Text();
export class PlaceholderView extends DOMNodeView {
}
PlaceholderView.__name__ = "PlaceholderView";
PlaceholderView.tag_name = "span";
export class Placeholder extends DOMNode {
    constructor(attrs) {
        super(attrs);
    }
    static init_Placeholder() {
        this.define(({}) => ({}));
    }
}
Placeholder.__name__ = "Placeholder";
Placeholder.init_Placeholder();
export class IndexView extends PlaceholderView {
    update(_source, i, _vars /*, formatters?: Formatters*/) {
        this.el.textContent = i.toString();
    }
}
IndexView.__name__ = "IndexView";
export class Index extends Placeholder {
    constructor(attrs) {
        super(attrs);
    }
    static init_Index() {
        this.prototype.default_view = IndexView;
        this.define(({}) => ({}));
    }
}
Index.__name__ = "Index";
Index.init_Index();
export class ValueRefView extends PlaceholderView {
    update(source, i, _vars /*, formatters?: Formatters*/) {
        const value = _get_column_value(this.model.field, source, i);
        const text = value == null ? "???" : `${value}`; //.toString()
        this.el.textContent = text;
    }
}
ValueRefView.__name__ = "ValueRefView";
export class ValueRef extends Placeholder {
    constructor(attrs) {
        super(attrs);
    }
    static init_ValueRef() {
        this.prototype.default_view = ValueRefView;
        this.define(({ String }) => ({
            field: [String],
        }));
    }
}
ValueRef.__name__ = "ValueRef";
ValueRef.init_ValueRef();
export class ColorRefView extends ValueRefView {
    render() {
        super.render();
        this.value_el = span();
        this.swatch_el = span({ class: styles.tooltip_color_block }, " ");
        this.el.appendChild(this.value_el);
        this.el.appendChild(this.swatch_el);
    }
    update(source, i, _vars /*, formatters?: Formatters*/) {
        const value = _get_column_value(this.model.field, source, i);
        const text = value == null ? "???" : `${value}`; //.toString()
        this.el.textContent = text;
    }
}
ColorRefView.__name__ = "ColorRefView";
export class ColorRef extends ValueRef {
    constructor(attrs) {
        super(attrs);
    }
    static init_ColorRef() {
        this.prototype.default_view = ColorRefView;
        this.define(({ Boolean }) => ({
            hex: [Boolean, true],
            swatch: [Boolean, true],
        }));
    }
}
ColorRef.__name__ = "ColorRef";
ColorRef.init_ColorRef();
export class DOMElementView extends DOMNodeView {
    constructor() {
        super(...arguments);
        this.child_views = new Map();
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        const children = this.model.children.filter((obj) => obj instanceof Model);
        await build_views(this.child_views, children, { parent: this });
    }
    render() {
        super.render();
        const { style } = this.model;
        if (style != null) {
            /*
            type IsString<T> = T extends string ? T : never
            type Key = Exclude<IsString<keyof CSSStyleDeclaration>,
              "length" | "parentRule" | "getPropertyPriority" | "getPropertyValue" | "item" | "removeProperty" | "setProperty">
            //this.el.style[key as Key] = value
            */
            if (style instanceof Styles) {
                for (const prop of style) {
                    const value = prop.get_value();
                    if (isString(value)) {
                        const name = prop.attr.replace(/_/g, "-");
                        if (this.el.style.hasOwnProperty(name)) {
                            this.el.style.setProperty(name, value);
                        }
                    }
                }
            }
            else {
                for (const [key, value] of entries(style)) {
                    const name = key.replace(/_/g, "-");
                    if (this.el.style.hasOwnProperty(name)) {
                        this.el.style.setProperty(name, value);
                    }
                }
            }
        }
        for (const child of this.model.children) {
            if (isString(child)) {
                const node = document.createTextNode(child);
                this.el.appendChild(node);
            }
            else {
                const child_view = this.child_views.get(child);
                child_view.renderTo(this.el);
            }
        }
    }
}
DOMElementView.__name__ = "DOMElementView";
export class DOMElement extends DOMNode {
    constructor(attrs) {
        super(attrs);
    }
    static init_DOMElement() {
        this.define(({ String, Array, Dict, Or, Nullable, Ref }) => ({
            style: [Nullable(Or(Ref(Styles), Dict(String))), null],
            children: [Array(Or(String, Ref(DOMNode), Ref(LayoutDOM))), []],
        }));
    }
}
DOMElement.__name__ = "DOMElement";
DOMElement.init_DOMElement();
export class ActionView extends View {
}
ActionView.__name__ = "ActionView";
export class Action extends Model {
    constructor(attrs) {
        super(attrs);
    }
    static init_Action() {
        this.define(({}) => ({}));
    }
}
Action.__name__ = "Action";
Action.__module__ = "bokeh.models.dom";
Action.init_Action();
export class TemplateView extends DOMElementView {
    constructor() {
        super(...arguments);
        this.action_views = new Map();
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        await build_views(this.action_views, this.model.actions, { parent: this });
    }
    remove() {
        remove_views(this.action_views);
        super.remove();
    }
    update(source, i, vars = {} /*, formatters?: Formatters*/) {
        function descend(obj) {
            for (const child of obj.child_views.values()) {
                if (child instanceof PlaceholderView) {
                    child.update(source, i, vars);
                }
                else if (child instanceof DOMElementView) {
                    descend(child);
                }
            }
        }
        descend(this);
        for (const action of this.action_views.values()) {
            action.update(source, i, vars);
        }
    }
}
TemplateView.__name__ = "TemplateView";
TemplateView.tag_name = "div";
export class Template extends DOMElement {
    static init_Template() {
        this.prototype.default_view = TemplateView;
        this.define(({ Array, Ref }) => ({
            actions: [Array(Ref(Action)), []],
        }));
    }
}
Template.__name__ = "Template";
Template.init_Template();
export class SpanView extends DOMElementView {
}
SpanView.__name__ = "SpanView";
SpanView.tag_name = "span";
export class Span extends DOMElement {
    static init_Span() {
        this.prototype.default_view = SpanView;
    }
}
Span.__name__ = "Span";
Span.init_Span();
export class DivView extends DOMElementView {
}
DivView.__name__ = "DivView";
DivView.tag_name = "div";
export class Div extends DOMElement {
    static init_Div() {
        this.prototype.default_view = DivView;
    }
}
Div.__name__ = "Div";
Div.init_Div();
export class TableView extends DOMElementView {
}
TableView.__name__ = "TableView";
TableView.tag_name = "table";
export class Table extends DOMElement {
    static init_Table() {
        this.prototype.default_view = TableView;
    }
}
Table.__name__ = "Table";
Table.init_Table();
export class TableRowView extends DOMElementView {
}
TableRowView.__name__ = "TableRowView";
TableRowView.tag_name = "tr";
export class TableRow extends DOMElement {
    static init_TableRow() {
        this.prototype.default_view = TableRowView;
    }
}
TableRow.__name__ = "TableRow";
TableRow.init_TableRow();
/////
import { RendererGroup } from "../renderers/renderer";
import { enumerate } from "../../core/util/iterator";
export class ToggleGroupView extends ActionView {
    update(_source, i, _vars /*, formatters?: Formatters*/) {
        for (const [group, j] of enumerate(this.model.groups)) {
            group.visible = i == j;
        }
    }
}
ToggleGroupView.__name__ = "ToggleGroupView";
export class ToggleGroup extends Action {
    constructor(attrs) {
        super(attrs);
    }
    static init_ToggleGroup() {
        this.prototype.default_view = ToggleGroupView;
        this.define(({ Array, Ref }) => ({
            groups: [Array(Ref(RendererGroup)), []],
        }));
    }
}
ToggleGroup.__name__ = "ToggleGroup";
ToggleGroup.init_ToggleGroup();
/*
export namespace X {
  export type Attrs = p.AttrsOf<Props>
  export type Props = Y.Props & {}
}

export interface X extends X.Attrs {}

export class X extends Y {
  override properties: X.Props

  constructor(attrs?: Partial<X.Attrs>) {
    super(attrs)
  }

  static init_X(): void {
    this.define<X.Props>(({}) => ({
    }))
  }
}
*/
//# sourceMappingURL=index.js.map