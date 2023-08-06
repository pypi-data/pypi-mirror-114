import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h } from 'preact';
import $ from "jquery";


class KrTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'columns': {}
        }
        this.paginateTo = this.paginateTo.bind(this);
    }

    componentDidMount() {
        let event = new CustomEvent('StateChange', {bubbles: true, detail: {'data': this.state}});
        this.base.dispatchEvent(event);
    }

    updateColumn(columnName, settings) {
        this.state.columns[columnName] = settings;
    }

    paginateTo(ev) {
        ev.preventDefault();

        this.state.paginate_to = ev.target.getAttribute('page');
        this.bubbleStateChange(ev);
    }

    doRender() {
        return <kr-table>
            <table {...this.props}>
                {this.props.children}
                <tfoot>
                    <tr>
                        <td colspan="1000">
                            <div style="width: 100%; margin-top: 1rem;">
                                {this.props.prevPage || this.props.nextPage ?
                                <nav style="float: center">
                                    <ul class="pagination pagination-lg">
                                        {this.props.prevPage ?
                                            <li class="page-item">
                                                <a class="page-link" page={this.props.prevPage} onClick={this.paginateTo}>&laquo;</a>
                                            </li>
                                            : <li class="page-item disabled">
                                                <a class="page-link">&laquo;</a>
                                            </li>
                                        }

                                        <li class="page-item"><a class="page-link" href="#">{this.props.actPage}</a></li>

                                        {this.props.nextPage ?
                                            <li class="page-item">
                                                <a class="page-link" page={this.props.nextPage} onClick={this.paginateTo}>&raquo;</a>
                                            </li>
                                            : <li class="page-item disabled">
                                                <a class="page-link">&raquo;</a>
                                            </li>
                                        }
                                    </ul>
                                </nav>
                                :
                                <nav style="float: center"></nav>
                                }
                            </div>
                        </td>
                    </tr>
                </tfoot>
            </table>
        </kr-table>
    }
}

registry.register('kr-table', KrTable);
export { KrTable }
