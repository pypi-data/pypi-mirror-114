import { Component} from "../../core/component";
import {registry} from "../..";
import { h } from 'preact';


class TopBarHeader extends Component {
    constructor(props) {
        super(props);
        this.setState({'isSideBarOpen': false});
        this.toggle = this.toggle.bind(this);
    }

    toggle() {
        if (this.state.isSideBarOpen === false) {
            this.props.class += ' show';
        } else {
            this.props.class = this.props.class.replace(' show', '');
        }

        this.setState({'isSideBarOpen': !this.state.isSideBarOpen});
    }

    render() {
        return <header { ...this.props }>
            <nav class="navbar navbar-expand-lg navbar-light" style="padding-top: 0; padding-bottom: 0;">
                <button class="navbar-toggler collapsed" type="button" onClick={this.toggle}>
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="container" style="padding-left: 0">
                    <div class="bg-primary collapse navbar-collapse" id="topbar">
                        <button class="navbar-toggler" type="button" onClick={this.toggle}>
                            X
                        </button>
                        { this.props.children }
                    </div>
                </div>
            </nav>
        </header>
    }
}
registry.register('kr-topbar-header', TopBarHeader);

class TopBarBody extends Component {
    render() {
        return <main class="container" style="padding-top: 15px;">{ this.props.children }</main>;
    }
}
registry.register('kr-topbar-body', TopBarBody);

class TopBarLayout extends Component {
    render() {
        return <kr-layout-topbar { ...this.props } style="padding: 0;">{ this.props.children }</kr-layout-topbar>;
    }
}

registry.register('kr-layout-topbar', TopBarLayout);

export { TopBarLayout, TopBarHeader, TopBarBody };