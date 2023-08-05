import { Range } from "./range";
export class DataRange extends Range {
    constructor(attrs) {
        super(attrs);
    }
    static init_DataRange() {
        this.define(({ String, Array, AnyRef }) => ({
            names: [Array(String), []],
            renderers: [Array(AnyRef( /*DataRenderer*/)), []], // TODO: [] -> "auto"
        }));
    }
}
DataRange.__name__ = "DataRange";
DataRange.init_DataRange();
//# sourceMappingURL=data_range.js.map