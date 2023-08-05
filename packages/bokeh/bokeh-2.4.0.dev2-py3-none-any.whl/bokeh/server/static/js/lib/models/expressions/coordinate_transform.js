import { Expression } from "../expressions/expression";
export class CoordinateTransform extends Expression {
    constructor(attrs) {
        super(attrs);
    }
    static init_CoordinateTransform() { }
    get x() {
        return new XComponent({ transform: this });
    }
    get y() {
        return new YComponent({ transform: this });
    }
}
CoordinateTransform.__name__ = "CoordinateTransform";
CoordinateTransform.init_CoordinateTransform();
export class XYComponent extends Expression {
    constructor(attrs) {
        super(attrs);
    }
    static init_XYComponent() {
        this.define(({ Ref }) => ({
            transform: [Ref(CoordinateTransform)],
        }));
    }
}
XYComponent.__name__ = "XYComponent";
XYComponent.init_XYComponent();
export class XComponent extends XYComponent {
    constructor(attrs) {
        super(attrs);
    }
    _v_compute(source) {
        return this.transform.v_compute(source).x;
    }
}
XComponent.__name__ = "XComponent";
export class YComponent extends XYComponent {
    constructor(attrs) {
        super(attrs);
    }
    _v_compute(source) {
        return this.transform.v_compute(source).y;
    }
}
YComponent.__name__ = "YComponent";
//# sourceMappingURL=coordinate_transform.js.map