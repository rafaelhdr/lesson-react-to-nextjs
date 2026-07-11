import Image from 'next/image'

export default function Home() {
  return (
    <div>
      <h1>Welcome to Four Devs Blog</h1>
      <Image
        src="/hello.jpg"
        alt="Hello"
        width={5784}
        height={3856}
        style={{ width: '100%', height: 'auto' }}
        priority
      />
      <p>
        This is a learning project to explore web development. Here you will find
        articles about Python, React, REST APIs, CSS, and Git — written for
        beginners who are just getting started.
      </p>
    </div>
  )
}
