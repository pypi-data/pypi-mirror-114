import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import {createRef, h, render,hydrate} from 'preact';
import $ from "jquery";


class KrAjaxPanel extends Component {
    constructor(props) {
        super(props);
        props.ref = createRef();
        this.handleStateChange = this.handleStateChange.bind(this);
        document.addEventListener('state-change', this.handleStateChange);
    }

    refreshContent() {
        $.post({
            url: this.props.contentUrl,
            data: this.state
        }).done((resp) => {
            let dom = resp;
            this.dataToCreateElement([dom]);
            this.props.children = dom[2];
            this.forceUpdate();
        });
    }

    doRender() {
        return <kr-ajax-panel {...this.props} onStateChange={this.handleStateChange} onReloadContent={this.handleStateChange}>{this.props.children}</kr-ajax-panel>;
    }

    handleStateChange(ev) {
        let data = this.state;
        $.extend(data, ev.detail.data);
        this.setState(data);
        if (ev.detail.forceUpdate === true) {
            this.refreshContent();
        }
    }

    componentDidMount() {
        /* this.base. */
        // window.addEventListener('state-change', this.handleStateChange);
    }
}

registry.register('kr-ajax-panel', KrAjaxPanel);

export { KrAjaxPanel }
