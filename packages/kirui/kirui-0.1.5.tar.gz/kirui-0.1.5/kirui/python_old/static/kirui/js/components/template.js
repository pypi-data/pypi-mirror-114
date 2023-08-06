import { Component, Element} from "../base/index.js"

const TEMPLATE = `valami`


export class TemplateLike extends Element {

}

let comp = new Component('kr-template', TEMPLATE)
comp.register(TemplateLike)
