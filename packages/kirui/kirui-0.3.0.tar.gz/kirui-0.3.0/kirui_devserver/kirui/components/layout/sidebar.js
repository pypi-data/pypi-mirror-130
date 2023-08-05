import {Component, registry} from "../..";
import { h } from 'preact';


class SidebarHeader extends Component {
    doRender() {
        return <div class="navbar fixed-top navbar-dark sidebar-header">
            <button class="navbar-toggler" type="button" style="margin-left: 2rem;">
                <span class="navbar-toggler-icon"></span>
            </button>
            { this.props.children }
        </div>
    }
}
registry.register('kr-sidebar-header', SidebarHeader);


class SidebarMenu extends Component {
    doRender() {
        return <div class="sidebar-menu">{ this.props.children }</div>
    }
}
registry.register('kr-sidebar-menu', SidebarMenu);

class SidebarBody extends Component {
    doRender() {
        return <div class="sidebar-body">{ this.props.children }</div>
    }
}
registry.register('kr-sidebar-body', SidebarBody);

class SidebarLayout extends Component {
    constructor() {
        super();
        this.state = {'loading': 'spinner-border d-none'}
        this.handleAjaxLoading = this.handleAjaxLoading.bind(this);
    }

    handleAjaxLoading(event) {
        event.stopPropagation();
        if (event.detail.loading === true) {
            this.setState({'loading': 'spinner-border'});
        } else {
            this.setState({'loading': 'spinner-border d-none'});
        }

    }

    doRender() {
        return <kr-layout-sidebar { ...this.props }>
            <div class="container-fluid" style="padding: 0; display: flex; margin-top: 54px;">
                { this.props.children }
            </div>
            <div id="loading" className={this.state.loading}>
                <span class="sr-only"></span>
            </div>
        </kr-layout-sidebar>;
    }

    componentDidMount() {
        this.base.addEventListener('AjaxLoading', this.handleAjaxLoading);
    }
}
registry.register('kr-layout-sidebar', SidebarLayout);

export { SidebarLayout, SidebarHeader, SidebarMenu };
