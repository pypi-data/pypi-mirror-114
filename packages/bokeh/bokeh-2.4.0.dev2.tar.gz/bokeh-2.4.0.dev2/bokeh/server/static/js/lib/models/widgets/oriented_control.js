import { Control, ControlView } from "./control";
import { Orientation } from "../../core/enums";
export class OrientedControlView extends ControlView {
    get orientation() {
        return this.model.orientation;
    }
}
OrientedControlView.__name__ = "OrientedControlView";
export class OrientedControl extends Control {
    constructor(attrs) {
        super(attrs);
    }
    static init_OrientedControl() {
        this.define(() => ({
            orientation: [Orientation, "horizontal"],
        }));
    }
}
OrientedControl.__name__ = "OrientedControl";
OrientedControl.init_OrientedControl();
//# sourceMappingURL=oriented_control.js.map