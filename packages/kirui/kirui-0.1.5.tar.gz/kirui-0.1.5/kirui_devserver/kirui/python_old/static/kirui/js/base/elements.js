import { Component } from './components.js'


export class Element {
    _component_config = Component

    connectedCallback() {
        this.shadow = this.attachShadow({mode: 'open'})
        
        if (document.adoptedStyleSheets !== undefined) {
            this.shadow.adoptedStyleSheets = document.adoptedStyleSheets
        } else {
            // TODO: implement
        }
    }
    
    render() {
        this.shadow.innerHTML = this._component_config.template.innerHTML
    }
}
