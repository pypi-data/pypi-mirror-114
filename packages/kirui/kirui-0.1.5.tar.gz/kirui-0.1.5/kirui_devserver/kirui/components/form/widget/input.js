import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h, Fragment } from 'preact';


class Input extends Component {
    beforeRender() {
        super.beforeRender();
        if (this.props.value) {
            let event = {
                target: {
                    'type': this.props.type,
                    'name': this.props.name,
                    'value': this.props.value
                }
            }
            this.props.onChange(event);
        }
    }

    doRender() {
        let cls = 'form-control'
        if (this.props.error) {
            cls += ' is-invalid'
        }
        return <Fragment>
            <input type="text" {...this.props} className={cls} />
            <div class="invalid-feedback">{this.props.error}</div>
        </Fragment>;
    }
}

registry.register('kr-form-input', Input);


class NumberInput extends Component {
    beforeRender() {
        super.beforeRender();
        if (this.props.value) {
            let event = {
                target: {
                    'type': this.props.type,
                    'name': this.props.name,
                    'value': this.props.value
                }
            }
            this.props.onChange(event);
        }
    }

    doRender() {
        let cls = 'form-control'
        if (this.props.error) {
            cls += ' is-invalid'
        }
        return <Fragment>
            <input type="number" {...this.props} className={cls} />
            <div class="invalid-feedback">{this.props.error}</div>
        </Fragment>;
    }
}

registry.register('kr-number-input', NumberInput);

export { Input, NumberInput };
