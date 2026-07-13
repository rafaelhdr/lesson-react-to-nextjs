import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

const API = 'http://localhost:8080'

function Post() {
  const { slug } = useParams()
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    fetch(`${API}/api/posts/${slug}`)
      .then((res) => {
        if (!res.ok) throw new Error('Post not found')
        return res.json()
      })
      .then((data) => {
        setPost(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [slug])

  if (loading) return <p>Loading...</p>
  if (error) return <p>{error}</p>

  return (
    <div>
      <Link to="/blog">← Back to Blog</Link>
      <h1>{post.title}</h1>
      <small>{post.date}</small>
      {post.content.split('\n\n').map((paragraph, i) => (
        <p key={i}>{paragraph}</p>
      ))}
    </div>
  )
}

export default Post
