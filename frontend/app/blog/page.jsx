import Link from 'next/link'

const API = 'http://localhost:5000'
const PER_PAGE = 2

export default async function Blog({ searchParams }) {
  const { page: pageParam } = await searchParams
  const page = Number(pageParam) || 1

  const res = await fetch(`${API}/api/posts?page=${page}&per_page=${PER_PAGE}`)
  const { posts, total_pages } = await res.json()

  return (
    <div>
      <h1>Blog</h1>

      {posts.map((post) => (
        <div key={post.id}>
          <h2>
            <Link href={`/blog/${post.slug}`}>{post.title}</Link>
          </h2>
          <p>{post.summary}</p>
          <small>{post.date}</small>
          <hr />
        </div>
      ))}

      <div>
        {page > 1 && <Link href={`?page=${page - 1}`}>Previous</Link>}
        {' '}Page {page} of {total_pages}{' '}
        {page < total_pages && <Link href={`?page=${page + 1}`}>Next</Link>}
      </div>
    </div>
  )
}
