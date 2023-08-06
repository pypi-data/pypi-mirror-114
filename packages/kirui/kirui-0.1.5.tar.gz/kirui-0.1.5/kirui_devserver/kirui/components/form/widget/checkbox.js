import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h, Fragment } from 'preact';


class CheckboxSwitch extends Component {
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
        let cls = 'form-control form-check-input'
        if (this.props.error) {
            cls += ' is-invalid'
        }

        if (this.props.value === true) {
            this.props.checked = true;
        }
        return <Fragment>
            <div class="form-check form-switch"><input type="checkbox" {...this.props} className={cls} /></div>
            <div class="invalid-feedback">{this.props.error}</div>
        </Fragment>;
    }
}

registry.register('kr-checkbox-switch', CheckboxSwitch);

export { CheckboxSwitch };
