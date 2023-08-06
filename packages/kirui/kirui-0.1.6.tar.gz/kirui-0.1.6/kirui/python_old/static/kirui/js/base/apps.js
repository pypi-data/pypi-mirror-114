
export class App {
    constructor() {
        this.components = []
    }

    component(klass) {
        this.components.push(klass)
    }

    mount(selector) {
        let el = document.querySelector(selector)
        console.log(el)
    }
}
