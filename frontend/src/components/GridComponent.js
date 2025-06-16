import React from 'react';

const BlockComponent = ({ block }) => {
    const style = {
        width: '20px',
        height: '20px',
        backgroundColor: block.colour || 'grey', // Default color if none provided
        display: 'inline-block',
        margin: '2px'
    };
    return <div style={style}></div>;
};

const ChemicalComponent = ({ chemicals }) => {
    // Simplified: Assume you transform chemicals to a color or gradient
    const color = 'blue'; // Placeholder: Compute based on chemicals
    const style = {
        width: '20px',
        height: '20px',
        backgroundColor: color,
        display: 'inline-block',
        margin: '2px'
    };
    return <div style={style} title={JSON.stringify(chemicals)}></div>;
};

const GridComponent = ({ env }) => {
    return (
        <div>
            <h2>Blocks Grid</h2>
            <div>
                {env.map((row, rowIndex) => (
                    <div key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                            <BlockComponent key={cellIndex} block={cell.block} />
                        ))}
                    </div>
                ))}
            </div>
            <h2>Chemicals Grid</h2>
            <div>
                {env.map((row, rowIndex) => (
                    <div key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                            <ChemicalComponent key={cellIndex} chemicals={cell.chemicals} />
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default GridComponent;
