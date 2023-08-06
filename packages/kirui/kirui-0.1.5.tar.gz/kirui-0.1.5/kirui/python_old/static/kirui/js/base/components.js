

export class Component {
    constructor(tag, template, options = {encapsulate_slots: false}) {
        this.tag = tag
        this.encapsulate_slots = options.encapsulate_slots
       
        let parser = new DOMParser()
        this.template = parser.parseFromString(template, 'text/html').body
    }
    
    register(klass) {
        klass.prototype._component_config = this
        customElements.define(this.tag, klass)
    }
}
