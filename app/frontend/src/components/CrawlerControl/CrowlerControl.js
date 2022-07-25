import React, { useState, useEffect } from 'react';
import './CrawlerControl.css';
import '../Loader/Loader.css';
import Task from '../Task/Task';
import Error from '../Error/Error';

function CrawlerControl() {
  const [url, setUrl] = useState("");
  const [onlyNestedToUrl, setOnlyNestedToUrl] = useState(false);
  const [nestingLimit, setNestingLimit] = useState(null);
  const [error, setError] = useState(null);
  const [tasks, setTasks] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const tasks = JSON.parse(localStorage.getItem('tasks'));
    if (tasks) {
     setTasks(tasks);
    }
  }, []);

  const crawlUrlHandler = async (url) => {
    setError(null)
    try {
      setIsLoading(true)

      const response = await fetch("/api/crawler/tasks", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'url': url,
          'nesting_limit': nestingLimit,
          'only_nested_to_url': onlyNestedToUrl
        })
      })

      const result = await response.json()
      const hash = result['result']['hash']
      const new_tasks = [{hash, url}, ...tasks]

      setTasks(new_tasks)

      localStorage.setItem('tasks', JSON.stringify(new_tasks));
    } catch {
      setError('Invalid URL')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="CrawlerControl">
      <Error error={error} />
      <h2 className="CrawlerHeader">Simple Web Crawler</h2>
      <div className="CrawlerInput">
        <div className="UrlInputBlock">
          <input
            type="number"
            placeholder="Nesting"
            className="NestingLimitInput"
            min={0}
            max={3}
            onChange={(e) => setNestingLimit(Number(e.target.value))}
            value={String(nestingLimit)}
          />
          <input
            type="url"
            placeholder="URL to crawl"
            className="UrlInput"
            onChange={(e) => setUrl(e.target.value)}
            value={url}
          />
          <button
            className="StartCrawlingButton"
            onClick={() => crawlUrlHandler(url)}
            disabled={nestingLimit === null || !url || isLoading}
          >
            {isLoading ? (<div className="Loader" /> ) : 'Go'}
          </button>
          <button
            className="ClearButton"
            onClick={() => {
              localStorage.removeItem('tasks')
              setTasks([])
            }}
          >
            Clear
          </button>
        </div>
        <div className="OnlyNestedToUrlBlock">
          <input
            className="OnlyNestedToUrlInput"
            type="checkbox"
            name="only_nested_to_url"
            checked={onlyNestedToUrl}
            onChange={() => setOnlyNestedToUrl(!onlyNestedToUrl)}
          />
          <label className="OnlyNestedToUrlLabel">Crawl only nested to the URL</label>
        </div>
      </div>
      <div className="TasksList">
        {
          tasks.map((task) =>
            <Task key={task['hash']} hash={task['hash']} url={task['url']} />)
        }
      </div>
    </div>
  );
}

export default CrawlerControl;
