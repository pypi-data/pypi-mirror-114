import { Expression } from "../expressions/expression";
import { ColumnarDataSource } from "../sources/columnar_data_source";
import { Arrayable } from "../../core/types";
import * as p from "../../core/properties";
export declare namespace CoordinateTransform {
    type Attrs = p.AttrsOf<Props>;
    type Props = Expression.Props;
}
export interface CoordinateTransform extends CoordinateTransform.Attrs {
}
export declare abstract class CoordinateTransform extends Expression<{
    x: Float64Array;
    y: Float64Array;
}> {
    properties: CoordinateTransform.Props;
    constructor(attrs?: Partial<CoordinateTransform.Attrs>);
    static init_CoordinateTransform(): void;
    get x(): XComponent;
    get y(): YComponent;
}
export declare namespace XYComponent {
    type Attrs = p.AttrsOf<Props>;
    type Props = Expression.Props & {
        transform: p.Property<CoordinateTransform>;
    };
}
export interface XYComponent extends XYComponent.Attrs {
}
export declare abstract class XYComponent extends Expression {
    properties: XYComponent.Props;
    constructor(attrs?: Partial<XYComponent.Attrs>);
    static init_XYComponent(): void;
}
export declare namespace XComponent {
    type Attrs = p.AttrsOf<Props>;
    type Props = XYComponent.Props;
}
export interface XComponent extends XComponent.Attrs {
}
export declare class XComponent extends XYComponent {
    properties: XComponent.Props;
    constructor(attrs?: Partial<XComponent.Attrs>);
    protected _v_compute(source: ColumnarDataSource): Arrayable<number>;
}
export declare namespace YComponent {
    type Attrs = p.AttrsOf<Props>;
    type Props = XYComponent.Props;
}
export interface YComponent extends YComponent.Attrs {
}
export declare class YComponent extends XYComponent {
    properties: YComponent.Props;
    constructor(attrs?: Partial<YComponent.Attrs>);
    protected _v_compute(source: ColumnarDataSource): Arrayable<number>;
}
//# sourceMappingURL=coordinate_transform.d.ts.map