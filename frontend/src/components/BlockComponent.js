const BlockComponent = ({ block }) => {
    const style = {
        width: '20px',
        height: '20px',
        backgroundColor: block.colour || 'grey', // Use block's color or default to grey
        display: 'inline-block',
        margin: '2px',
        border: '1px solid white' // Add border to distinguish blocks
    };

    return <div style={style} title={`Energy: ${block.energy || 'N/A'}`}></div>; // Tooltip showing energy
};

export default BlockComponent