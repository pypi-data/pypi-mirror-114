import { Component} from "../../core/component";
import {registry} from "../..";
import { h } from 'preact';


class App extends Component {
    render() {
        return <kr-app { ...this.props }>{ this.props.children }</kr-app>;
    }
}

registry.register('kr-app', App);

export { App };
