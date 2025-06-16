const ChemicalComponent = ({ chemicals }) => {
    // Placeholder: Assuming chemicals object has keys representing chemical types
    // and values representing concentrations. Adjust based on your actual data structure.
    const titles = Object.entries(chemicals).map(([key, value]) => `${key}: ${value}`).join(', ');

    const highestConcentration = Math.max(...Object.values(chemicals));
    const colorIntensity = highestConcentration * 255; // Example calculation
    const color = `rgb(${colorIntensity}, 0, 0)`; // Example: more concentration, more red

    const style = {
        width: '20px',
        height: '20px',
        backgroundColor: color,
        display: 'inline-block',
        margin: '2px',
        border: '1px solid white' // Add border to distinguish chemicals
    };

    return <div style={style} title={titles}></div>; // Tooltip showing chemical details
};

export default ChemicalComponent