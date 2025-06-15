import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const processData = (data) => {
    const labels = Array.from({ length: data.length }, (_, i) => i + 1);
    const datasets = {};

    data.forEach((dict, index) => {
        for (let [key, value] of Object.entries(dict)) {
            if (!datasets[key]) {
                datasets[key] = {
                    label: key,
                    data: Array(data.length).fill(null),
                    borderColor: getRandomColor(),
                    borderWidth: 1,
                    fill: false
                };
            }
            datasets[key].data[index] = value;
        }
    });

    return {
        labels: labels,
        datasets: Object.values(datasets)
    };
};

const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
};

const ChemicalCountGraph = ({ total_count }) => {
    const chartData = processData(total_count);
    return (
        <div>
            <h2>Line Chart of total_count Data</h2>
            <Line
                data={chartData}
                options={{
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Chart.js Line Chart'
                        }
                    }
                }}
            />
        </div>
    );
};

export default ChemicalCountGraph;