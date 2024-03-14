import { useEffect, useState } from 'react';
import './App.css';
import React from 'react';

function App() {
  const [data, setData] = useState({
    greeting: '',
  });
  const [keyword, setKeyword] = useState('');
  const [year, setYear] = useState('');

  const request = {
    keyword: keyword,
    year: year,
  };

  useEffect(() => {
    console.log('use effect');
    fetch('http://127.0.0.1:5000/', {
      headers: {
        'Content-Type': 'application/json',
      },
    }).then((res) =>
      res.json().then((data) => {
        setData({
          greeting: data.greeting,
        });
      })
    );
  }, []);

  async function postData(url: string, request: object) {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      referrerPolicy: 'no-referrer',
      body: JSON.stringify(request),
    });
    return response.json();
  }

  const clickHandler = () => {
    console.log('submitted', keyword, year);
    postData('http://127.0.0.1:5000/search', request).then((data) => console.log(data.response));
  };

  return (
    <>
      <h1>calendar-parse</h1>
      <h2>Search keywords:</h2>
      <input type='text' value={keyword} onChange={(e) => setKeyword(e.target.value)} />
      <h2>Add year:</h2>
      <div>
        <input type='text' value={year} onChange={(e) => setYear(e.target.value)} />
      </div>
      <button onClick={() => clickHandler()}>Submit</button>
      <div className='card'>
        <p>{data?.greeting}</p>
        <h3>{keyword.toUpperCase()}</h3>
        <h3>{year}</h3>
      </div>
    </>
  );
}

export default App;
