import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h, Fragment } from 'preact';


class Select extends Component {
    beforeRender() {
        super.beforeRender();
        // ha a value-ban jön érték, vagy az első választás nem null
        if ((this.props.value) || ((this.props.value === null) && (this.props.children[0].props.value !== null))) {
            let event = {
                target: {
                    'type': this.props.type,
                    'name': this.props.name,
                    'value': this.props.value || this.props.children[0].props.value
                }
            }
            this.props.onChange(event);
        }
    }

    doRender() {
        let cls = 'form-select'
        if (this.props.error) {
            cls += ' is-invalid'
        }
        return <Fragment>
            <select className={cls} {...this.props}>
                {this.props.children}
            </select>
            <div class="invalid-feedback">{this.props.error}</div>
        </Fragment>
    }
}

registry.register('kr-form-select', Select);

export { Select };
