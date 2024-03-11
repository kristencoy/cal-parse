import { useEffect, useState } from 'react';
import './App.css';
import React from 'react';

function App() {
  const [data, setData] = useState({
    greeting: '',
  });
  const [keyword, setKeyword] = useState('');
  const [year, setYear] = useState('');

  useEffect(() => {
    console.log('use effect');
    fetch('http://127.0.0.1:5000/').then((res) =>
      res.json().then((data) => {
        setData({
          greeting: data.greeting,
        });
      })
    );
  }, []);

  const clickHandler = () => {
    console.log('submitted', keyword, year);
  };

  return (
    <>
      <h1>Search keywords:</h1>
      <input type='text' value={keyword} onChange={(e) => setKeyword(e.target.value)} />
      <h1>Add year span:</h1>
      <input type='text' value={year} onChange={(e) => setYear(e.target.value)} />
      <span> - </span>
      <input type='text' />
      <button
        onClick={() => clickHandler()}
        style={{ display: 'block', marginLeft: '10rem', marginTop: '1rem' }}
      >
        Submit
      </button>
      <div className='card'>
        <p>{data.greeting}</p>
        <h3>{keyword.toUpperCase()}</h3>
        <h3>{year}</h3>
      </div>
    </>
  );
}

export default App;
