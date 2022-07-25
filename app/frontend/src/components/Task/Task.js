import React, { useState, useEffect } from 'react';
import './Task.css';
import Error from '../Error/Error';

function Task({ hash, url }) {
  const [error, setError] = useState(null);
  const [crawledUrls, setCrawledUrls] = useState([]);
  const [numberOfProcessedURLs, setNumberOfProcessedURLs] = useState(0);
  const [status, setStatus] = useState('...');

  useEffect(() => {
    const intervalId = setInterval(async () => {
      const status = await getStatus(hash)
      setStatus(status['result']['job_status'])
      setNumberOfProcessedURLs(status['result']['number_of_urls'])
      if (
        status['result']['job_status'] === 'Done' ||
        status['result']['job_status'] === 'Not exist'
      ) {
        clearInterval(intervalId)
        const result = await getResults(hash)
        setCrawledUrls(result['result']['urls'])
      }
    }, 1000)
    return () => clearInterval(intervalId)
  }, [hash])

  const getResults = async (hash) => {
    try {
      const response = await fetch(`/api/crawler/tasks?hash=${hash}`)
      return await response.json()
    } catch {
      setError('Error while fetching result')
    }
  }

  const getStatus = async (hash) => {
    try {
      const response = await fetch(`/api/crawler/tasks/status?hash=${hash}`)
      return await response.json()
    } catch {
      setError('Error while fetching status')
    }
  }

  return (
    <div className="TaskBlock">
      <Error error={error} />
      <div className="TaskInfoBlock">
        <div className="TaskInfo">URL: <b>{url}</b></div>
        <div className="TaskInfo">Status: <b>{status}</b></div>
        <div className="TaskInfo">Number of crawled URLs: <b>{numberOfProcessedURLs}</b></div>
      </div>
      <textarea
        className="CrawledUrls"
        value={crawledUrls.length > 0 ? crawledUrls.join('\n') : 'URLs will be here'}
      />
    </div>
  );
}

export default Task;
