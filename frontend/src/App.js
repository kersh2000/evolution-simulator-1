import React, { useState, useEffect } from 'react';
import BlockComponent from './components/BlockComponent.js'
import ChemicalComponent from './components/ChemicalComponent.js'
import ChemicalCountGraph from './components/ChemicalCount.js';

// BlockComponent and ChemicalComponent remain the same as before

const GridComponent = () => {
    const [env, setEnv] = useState([]);
    const [totalCountData, setTotalCountData] = useState([]);
    const [isFetching, setIsFetching] = useState(false);

    useEffect(() => {
        const fetchData = () => {
            fetch('http://127.0.0.1:8000/code')
                .then(response => response.json())
                .then(data => setEnv(data.env))
                .catch(error => console.error('Error fetching data: ', error));
        };

        fetchData();
    }, []);

    useEffect(() => {
        let intervalId;
        if (isFetching) {
            intervalId = setInterval(() => {
                fetch('http://127.0.0.1:8000/step', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ env }),
                })
                .then(response => response.json())
                .then(data => { 
                    setTotalCountData(data.total_count)
                    setEnv(data.env)
                })
                .catch(error => console.error('Error updating env: ', error));
            }, 500);
        }

        return () => {
            if (intervalId) clearInterval(intervalId);
        };
    }, [isFetching, env]); // Depend on isFetching and env


    const handleStep = () => {
      fetch('http://127.0.0.1:8000/step', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ env }),
      })
      .then(response => response.json())
      .then(data => { 
        setTotalCountData(data.total_count)
        setEnv(data.env)
        })
      .catch(error => console.error('Error updating env: ', error));
    };

    const startFetching = () => setIsFetching(true);
    const stopFetching = () => setIsFetching(false);

    const handleSteps = (steps) => {
        fetch(`http://127.0.0.1:8000/step/${steps}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ env }),
        })
        .then(response => response.json())
        .then(data => { 
            setTotalCountData(data.total_count)
            setEnv(data.env)
        })
        .catch(error => console.error('Error updating env: ', error));
      };

    return (
        <div>
            <button onClick={handleStep}>Step</button>
            <button onClick={startFetching} disabled={isFetching}>Start</button>
            <button onClick={stopFetching} disabled={!isFetching}>Stop</button>
            <button onClick={() => {handleSteps(10)}}>Step 10</button>
            <button onClick={() => {handleSteps(25)}}>Step 25</button>
            <button onClick={() => {handleSteps(100)}}>Step 100</button>
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
            <ChemicalCountGraph total_count={totalCountData} />
        </div>
    );
};

export default GridComponent;
