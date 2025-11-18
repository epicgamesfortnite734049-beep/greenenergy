import React from 'react';
import { ChartDataPoint } from '../types';

interface CarbonChartProps {
    data: ChartDataPoint[];
    title: string;
}

const COLORS = ['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800'];

const CarbonChart: React.FC<CarbonChartProps> = ({ data, title }) => {
    if (!data || data.length === 0) return null;

    const totalValue = data.reduce((sum, item) => sum + item.value, 0);

    const getCoordsOnCircle = (angle: number, radius: number) => {
        const radians = (angle - 90) * Math.PI / 180.0;
        return {
            x: 50 + (radius * Math.cos(radians)),
            y: 50 + (radius * Math.sin(radians))
        };
    };

    const describeArc = (radius: number, startAngle: number, endAngle: number): string => {
        // Handle the case of a full circle
        if (Math.abs(endAngle - startAngle) >= 359.99) {
            const center = 50;
            const r = radius;
            return `M ${center},${center - r} a ${r},${r} 0 1,1 0,${2 * r} a ${r},${r} 0 1,1 0,-${2 * r}`;
        }
        
        const start = getCoordsOnCircle(startAngle, radius);
        const end = getCoordsOnCircle(endAngle, radius);
        const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";

        return [
            "M", 50, 50, // Move to center
            "L", start.x, start.y, // Line to start of arc
            "A", radius, radius, 0, largeArcFlag, 1, end.x, end.y, // Arc to end
            "Z" // Close path
        ].join(" ");
    };

    let cumulativeAngle = 0;

    return (
        <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <h4 className="text-sm font-bold text-gray-800 dark:text-white mb-3 text-center">
                {title}
            </h4>
            <div className="flex flex-col md:flex-row items-center justify-center gap-4">
                <div className="w-40 h-40 flex-shrink-0">
                    <svg viewBox="0 0 100 100" className="transform -rotate-90">
                        {data.map((item, index) => {
                            const percentage = (item.value / totalValue);
                            const sweepAngle = percentage * 360;
                            const startAngle = cumulativeAngle;
                            const endAngle = startAngle + sweepAngle;
                            const pathData = describeArc(45, startAngle, endAngle);
                            cumulativeAngle = endAngle;

                            return (
                                <path
                                    key={item.source}
                                    d={pathData}
                                    fill={COLORS[index % COLORS.length]}
                                >
                                    <title>{`${item.source}: ${item.value.toLocaleString()} kg CO₂ (${(percentage * 100).toFixed(1)}%)`}</title>
                                </path>
                            );
                        })}
                         <circle cx="50" cy="50" r="20" fill="white" className="dark:fill-gray-800" />
                    </svg>
                </div>
                <div className="flex flex-col justify-center space-y-2 text-xs">
                    {data.map((item, index) => (
                        <div key={item.source} className="flex items-center">
                            <span
                                className="h-3 w-3 rounded-sm mr-2"
                                style={{ backgroundColor: COLORS[index % COLORS.length] }}
                            ></span>
                            <span className="font-medium text-gray-700 dark:text-gray-300">{item.source}:</span>
                            <span className="ml-1 text-gray-600 dark:text-gray-400">{item.value.toLocaleString()} kg CO₂</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default CarbonChart;
