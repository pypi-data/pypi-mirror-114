import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h } from 'preact';
import $ from "jquery";

class KrRows extends Component {
    doRender() {
        return <tbody>
            {this.props.children}
        </tbody>
    }
}

class KrRow extends Component {
    doRender() {
        return <tr>{this.props.children}</tr>
    }
}

class KrCell extends Component {
    doRender() {
        return <td {...this.props}>{this.props.children}</td>
    }
}

registry.register('kr-rows', KrRows);
registry.register('kr-row', KrRow);
registry.register('kr-cell', KrCell);
export { KrRows, KrRow, KrCell }
