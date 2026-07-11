import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const API = 'http://localhost:5000'
const PER_PAGE = 2

function Blog() {
  const [posts, setPosts] = useState([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetch(`${API}/api/posts?page=${page}&per_page=${PER_PAGE}`)
      .then((res) => res.json())
      .then((data) => {
        setPosts(data.posts)
        setTotalPages(data.total_pages)
        setLoading(false)
      })
  }, [page])

  return (
    <div>
      <h1>Blog</h1>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          {posts.map((post) => (
            <div key={post.id}>
              <h2>
                <Link to={`/blog/${post.slug}`}>{post.title}</Link>
              </h2>
              <p>{post.summary}</p>
              <small>{post.date}</small>
              <hr />
            </div>
          ))}

          <div>
            <button onClick={() => setPage((p) => p - 1)} disabled={page === 1}>
              Previous
            </button>
            {' '}Page {page} of {totalPages}{' '}
            <button onClick={() => setPage((p) => p + 1)} disabled={page === totalPages}>
              Next
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default Blog
