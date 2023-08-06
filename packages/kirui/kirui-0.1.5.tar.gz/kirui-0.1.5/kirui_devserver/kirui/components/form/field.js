import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h } from 'preact';


class FormField extends Component {
    constructor(props) {
        super(props);
    }

    doRender() {
        let label;
        if (this.props.label) {
            let cls = 'col-form-label'
            if (this.props['label-width']) {
                for (let part of this.props['label-width'].split(' ')) {
                    cls += ' col-' + part;
                }
                delete this.props['label-width']
            }

            if (this.props.required) {
                cls += ' required';
            }
            delete this.props.required;

            label = <label for={this.props.id} className={cls}>{this.props.label}</label>;
            delete this.props.label;
        }

        let cls = '';
        if (this.props['field-width']) {
            for (let part of this.props['field-width'].split(' ')) {
                cls += ' col-' + part;
            }
            delete this.props['field-width']
        } else {
            cls = 'col'
        }

        let el = registry.getComponent(this.props.widget);
        el = h(...[el, this.props, this.props.children]);
        delete this.props.widget;

        return <div class="mb-3 row">
            {label}
            <div className={cls}>
                {el}
            </div>
        </div>
    }
}

registry.register('kr-form-field', FormField);
export { FormField }