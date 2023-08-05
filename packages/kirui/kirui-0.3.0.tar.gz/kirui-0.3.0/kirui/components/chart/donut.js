import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { Component } from "../../core/component";
import { registry } from "/kirui/core/registry";
import { h } from 'preact';

ChartJS.register(ArcElement, Tooltip, Legend);


class KrDonutChart extends Component {
    constructor() {
        super();
        this.colors = [
            'rgb(23, 118, 182)',
            'rgb(255, 127, 0)',
            'rgb(150,224,134)',
            'rgb(216,36,31)',
            'rgb(255, 188, 114)',
            'rgb(149,100,191)',
            'rgb(141,86,73)',
            'rgb(173, 198, 233)',
            'rgb(197,175,214)',
            'rgb(197,156,147)',
            'rgb(229,116,195)',
            'rgb(36,162,33)',
            'rgb(255,151,148)',
        ]
    }
    doRender() {
        let data = {'labels': [], 'datasets': [{'data': [], 'backgroundColor': []}]};

        let counter = 0;
        for (let [k, v] of Object.entries(this.props.values)) {
            data['labels'].push(k);
            data['datasets'][0]['data'].push(v);
            let color = this.colors[counter];
            if (color === undefined) {
                counter = 1;
                color = this.colors[counter];
            }

            data['datasets'][0]['backgroundColor'].push(color);
            counter = counter + 1;
        }

        return <Doughnut data={data} />;
    }
}

registry.register('kr-chart-donut', KrDonutChart);

export { KrDonutChart }
