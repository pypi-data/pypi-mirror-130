import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import {createRef, h, render} from 'preact';
import { evaluate } from '/kirui/core/element';
import $ from "jquery";


class SideModal extends Component {
    constructor(props) {
        super(props);
        this.setState({'display': 'block'});
        this.hide = this.hide.bind(this);
    }

    hide() {
        $('body').removeClass('focus-hidden');
        this.setState({'display': 'none'});
        this.parent.closeModal();
    }

    show() {
        this.setState({'display': 'block'});
        this.forceUpdate();
    }

    doRender() {
        return <kr-side-modal style={{display: this.state.display }}>
            <div class="overlay"></div>
            <div class="modal" { ...this.props }>
            { this.props.children }
            </div>
        </kr-side-modal>
    }
}
registry.register('kr-side-modal', SideModal);


class ModalHeader extends Component {
    constructor(props) {
        super(props);
        this.hide = this.hide.bind(this);
    }

    hide() {
        let e = new CustomEvent('CloseModal', {'bubbles': true});
        this.base.dispatchEvent(e);
    }

    doRender() {
        return <div class="header">
            <div class="modal-title">{ this.props.children }</div>
            <button type="button" class="btn-close" onClick={this.hide}></button>
        </div>
    }
}
registry.register('kr-modal-header', ModalHeader);

class ModalBody extends Component {
    doRender() {
        return <div class="body"><div class="col">{ this.props.children }</div></div>
    }
}
registry.register('kr-modal-body', ModalBody);

class ModalFooter extends Component {
    doRender() {
        return <div class="footer">{ this.props.children }</div>
    }
}
registry.register('kr-modal-footer', ModalFooter);


class ModalLink extends Component {
    constructor(props) {
        super(props);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        document.addEventListener('CloseModal', this.closeModal);
    }

    handleSubmit(event) {
        event.preventDefault();
        event.stopPropagation();
        if (event.detail['force_update'] === false) {
            return;
        }

        let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': true}});
        this.base.dispatchEvent(e);

        $.post({
          url: this.props.href,
          data: $.param(event.detail.data, true),
        }).fail((resp) => {
            if (resp.status === 403) {
                let d = evaluate(resp.responseText);
                this.setState({'modal': d});
                $('body').addClass('focus-hidden');
                let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
                this.base.dispatchEvent(e);
            }
        }).done((resp) => {
            this.closeModal();
            let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
            this.base.dispatchEvent(e);

            if (this.props.bubbleSuccessEvent && this.props.bubbleSuccessEvent.length) {
                let ev = new CustomEvent(this.props.bubbleSuccessEvent, {bubbles: true, detail: {forceUpdate: true}});
                this.base.dispatchEvent(ev);
            }
        })
    }

    openModal(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': true}});
        this.base.dispatchEvent(e);

        let url = ev.target.getAttribute('url');
        $.get({
          url: this.props.href,
          contentType: "application/json",
        }).fail((resp) => {
            if (resp.status === 403) {
                let d = evaluate(resp.responseText);
                this.setState({'modal': d});
                $('body').addClass('focus-hidden');
                let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
                this.base.dispatchEvent(e);
            }
        }).done((resp) => {
            let d = evaluate(resp.responseText);
            this.setState({'modal': d});
            $('body').addClass('focus-hidden');
            let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
            this.base.dispatchEvent(e);
        });
    }

    componentDidMount() {
        this.base.addEventListener('StateChange', this.handleSubmit);
    }

    closeModal(ev) {
        if (ev !== undefined) {
            ev.stopPropagation();
        }

        $('body').removeClass('focus-hidden');
        this.setState({'modal': null});
    }

    doRender() {
        return <div><a onClick={this.openModal} { ...this.props }>{ this.props.children }</a>{ this.state.modal }</div>
    }
}
registry.register('kr-modal-link', ModalLink);

export { SideModal, ModalHeader, ModalBody, ModalFooter, ModalLink }
