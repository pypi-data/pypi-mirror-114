import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h, Fragment, createRef } from 'preact';
import $ from "jquery";


class MultiSelectOption extends  Component {
    doRender() {
        return <li {...this.props}><input type="checkbox" checked={this.props.selected} value={this.props.value} />{this.props.children}</li>
    }
}

class MultiSelectCheckbox extends Component {
    constructor(props) {
        super(props);
        this.state = {'value': new Set(), 'display': false};
        this.changeState = this.changeState.bind(this);
        this.toggleDropDown = this.toggleDropDown.bind(this);
        this.handleClickOutside = this.handleClickOutside.bind(this);
        this.myRef = createRef();

        let trues = new Set(['true', '1', 1, true]);
        for (let child of this.props.children) {
            if (trues.has(child.props.selected)) {
                this.state.value.add(child.props.value);
            }
        }
    }

    getOptions() {
        let retval = [];
        for (let child of this.props.children) {
            child.props.selected = this.state.value.has(child.props.value);
            let c = <MultiSelectOption onClick={this.changeState} {...child.props}>{child.props.children}</MultiSelectOption>
            retval.push(c);
        }

        return retval;
    }

    getLabel() {
        let label = '';
        for (let child of this.props.children) {
            if (this.state.value.has(child.props.value)) {
                label += child.props.children[0] + ', '
            }
        }

        if (label === '') {
            label = this.props.title || 'Select options...';
        } else {
            label = label.substring(0, label.length - 2);
        }

        return label;
    }

    changeState(ev) {
        ev.stopPropagation();
        let value = ev.target.value.toString();

        let lastState = this.state.value;

        if (lastState.has(value)) {
            lastState.delete(value);
        } else {
            lastState.add(value);
        }

        this.setState({'value': lastState});
        let params = {bubbles: true, detail: {'data': Array.from(lastState), 'target': this.base}}
        let event = new CustomEvent('HandleInputChange', params);
        this.base.dispatchEvent(event);
    }

    toggleDropDown(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const {display} = this.state.display;
        this.setState({display:!display});
        window.addEventListener('mousedown', this.handleClickOutside, false);
    }

    handleClickOutside(event) {
        if(this.myRef && !this.myRef.current.contains(event.target)){
            this.setState({display:false});
            window.removeEventListener('mousedown', this.handleClickOutside, false);
        }
    }

    componentWillUnmount(){
        window.removeEventListener('mousedown', this.handleClickOutside, false);
    }

    doRender() {
        let cls = 'form-select'
        if (this.props.error) {
            cls += ' is-invalid'
        }

        return <Fragment>
            <kr-multi-select-checkbox {...this.props} ref={this.myRef}>
                <button onClick={this.toggleDropDown} className={cls}>
                    {this.getLabel()}
                </button>
                {
                    this.state.display && (
                        <div className="choices" onStateChange={this.changeState}>
                            <ul>
                                {this.getOptions()}
                            </ul>
                        </div>
                    )
                }
            </kr-multi-select-checkbox>
            <div class="invalid-feedback" style="display: inline-block">{this.props.error}</div>
        </Fragment>
    }

    componentDidMount() {
        let params = {bubbles: true, detail: {'data': Array.from(this.state.value), 'target': this.base}}
        let event = new CustomEvent('HandleInputChange', params);
        this.base.dispatchEvent(event);
    }
}

registry.register('kr-multi-select-checkbox', MultiSelectCheckbox);

export { MultiSelectCheckbox, MultiSelectOption };
