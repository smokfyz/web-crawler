import './Error.css'

function Error({ error }) {
  if (!error)
    return null

  return (
    <div className="Error">
      {error}
    </div>
  )
}

export default Error;
