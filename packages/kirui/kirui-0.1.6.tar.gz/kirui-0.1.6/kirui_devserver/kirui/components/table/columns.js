import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h } from 'preact';
import $ from "jquery";


class KrColumns extends Component {
    constructor(props) {
        super(props);
    }

    doRender() {
        return <thead><tr>
            {this.props.children}
        </tr></thead>
    }
}

class KrColumn extends Component {
    componentDidMount() {
        let table = this.parents('kr-table');
        table.updateColumn(this.props.id, {})
    }

    doRender() {
        return <th {...this.props}>{this.props.children}</th>
    }
}

registry.register('kr-columns', KrColumns);
registry.register('kr-column', KrColumn);
export { KrColumns, KrColumn }
