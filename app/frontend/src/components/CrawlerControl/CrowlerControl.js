import React, { useState } from 'react';
import './CrawlerControl.css';

function CrawlResult({ crawledUrls }) {
  if (!crawledUrls)
    return null

  return (
    <div className="CrawlResult">
      {crawledUrls.map((url) => <a className="CrawledLink" href={url}>{url}</a>)}
    </div>
  )
}

function CrawlerControl() {
  const [url, setUrl] = useState("");
  const [crawledUrls, setCrawledUrls] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const crawlUrlHandler = async () => {
    if (isLoading)
      return

    setIsLoading(true)

    const response = await fetch("/api/crawler/tasks", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        url
      })
    })
    const result = await response.json()

    setCrawledUrls(result['urls'])
    setIsLoading(false)
  }

  return (
    <div className="CrawlerControl">
      <h2 className="CrawlerHeader">Simple Web Crawler</h2>
      <div className="CrawlerInput">
        <input
          type="url"
          placeholder="URL to crawl"
          className="UrlInput"
          onChange={(e) => setUrl(e.target.value)}
          value={url}
        />
        <button
          className="StartCrawlingButton"
          onClick={crawlUrlHandler}
          disabled={!url}
        >
          Go
        </button>
      </div>
      {isLoading ? <div className="Loader" /> : <CrawlResult crawledUrls={crawledUrls} />}
    </div>
  );
}

export default CrawlerControl;
