import { Component as PreactComponent, h } from 'preact';
import { registry } from './registry';
import $ from "jquery";


class Component extends PreactComponent {
    static tagName = null;

    componentWillMount() {
        this.parent = this.props['kr:parent'];
        delete this.props['kr:parent'];

        for (let child of this.props.children) {
            if (child.props !== undefined) {
                child.props['kr:parent'] = this;
            }
        }
    }

    parents(tagName) {
        let p = this.parent;
        while (true) {
            if (p === undefined) {
                return p;
            }

            if (p.tagName === tagName) {
                return p;
            }

            p = p.parent;
        }
    }

    beforeRender() {
        /* Update context */
        if (this.props.reactContextRef) {
            this.context[this.props.reactContextRef] = this;
        }

        /* Bind events */
        for (let event_name of ['onChange', 'onSubmit']) {
            if ((typeof this.props[event_name]) === 'string') {
                let [context_var, callable] = this.props[event_name].split('.');
                if (context_var == 'this') {
                    this.props[event_name] = this[callable];
                } else {
                    this.props[event_name] = this.context[context_var][callable];
                }
            }
        }
    }

    setState(state, callback) {
        super.setState(state, callback);
        if ((typeof this.props.reactDelegateStateTo  == 'string') && (this.props.reactDelegateStateTo.length > 0)) {
            /* A this.state itt az előző állapotot mutatja, az aktuális állapotot én kanalazom össze */
            let data = this.context[this.props.reactDelegateStateTo].state;
            // console.log(data);
            // console.log(state);
            $.extend(data, state);
            // {[this.props.reactContextRef]: data}
            // console.log(data);
            this.context[this.props.reactDelegateStateTo].setState(data);
        }
    }

    bubbleStateChange(orig_event) {
        let params = {bubbles: true, detail: {'data': this.state}}

        if (orig_event !== undefined) {
            orig_event.preventDefault();
            params.detail.forceUpdate = true;
        } else {
            params.detail.forceUpdate = false;
        }

        let event = new CustomEvent('StateChange', params);
        this.base.dispatchEvent(event);
    }

    doRender() {
        return h(this.tagName, this.props, this.props.children);
    }

    render() {
        this.beforeRender();
        return this.doRender();
    }
}

const html_element = (tag_name) => {
    /*
        TODO: optimalizálni. Ez minden gyermekhez legyárt egy külön osztályt. Jobb lenne function base component-el helyettesíteni.
        Azzal viszont az a szopás, hogy a this.context-et nem érem el.
     */
    return class Comp extends PreactComponent {
        tagName = tag_name;

        render() {
            if (this.props.onClick !== undefined) {
                let [context_var, callable] = this.props.onClick.split('.');
                this.props.onClick = this.context[context_var][callable];
            }

            return h(this.tagName, this.props, this.props.children);
        }
    }
}

Component.prototype.dataToCreateElement = (iterable) => {
    for (let i = 0; i < iterable.length; i++) {
        let el = iterable[i];
        if (typeof el !== 'string') {
            // ['tag-name', props, children]
            let component = registry.getComponent(el[0]);
            if (component === undefined) {  // not registered component
                el[0] = html_element(el[0]);
                Component.prototype.dataToCreateElement(el[2]);
            } else {  // registered component
                el[0] = registry.getComponent(el[0]);
                Component.prototype.dataToCreateElement(el[2]);
            }
            el = h(...el);
        }
        // console.log(el.props);
        iterable[i] = el;
    }
}

export { Component };
