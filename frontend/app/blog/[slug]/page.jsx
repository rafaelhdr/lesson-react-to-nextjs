import Link from 'next/link'

const API = 'http://localhost:5000'

export default async function Post({ params }) {
  const { slug } = await params
  const res = await fetch(`${API}/api/posts/${slug}`)

  if (!res.ok) return <p>Post not found</p>

  const post = await res.json()

  return (
    <div>
      <Link href="/blog">← Back to Blog</Link>
      <h1>{post.title}</h1>
      <small>{post.date}</small>
      {post.content.split('\n\n').map((paragraph, i) => (
        <p key={i}>{paragraph}</p>
      ))}
    </div>
  )
}
