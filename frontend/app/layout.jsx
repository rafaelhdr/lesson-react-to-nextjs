import Link from 'next/link'
import './globals.css'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav>
          <Link href="/">Home</Link>
          {' | '}
          <Link href="/blog">Blog</Link>
        </nav>
        <main>
          {children}
        </main>
      </body>
    </html>
  )
}
