from flask import Flask, jsonify, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

posts = [
    {
        "id": 12,
        "slug": "deploying-to-production",
        "title": "Deploying to Production",
        "summary": "How to build and run both the Flask backend and the Next.js frontend for production.",
        "content": """Running the app with npm run dev and python app.py is fine for development, but neither is meant for production. Here is how to run both properly.

For the frontend, run npm run build inside the frontend folder. Next.js compiles and optimises all pages into the .next folder. Once that is done, run npm start. That starts the Next.js production server, which serves the built output. It handles routing, server components, and image optimisation the same way as dev, but faster and without the hot-reload overhead. By default it listens on port 3000.

For the backend, Flask's built-in server is also not production-ready. The standard replacement is gunicorn. Install it with pip install gunicorn, then run gunicorn app:app from inside the backend folder. This starts a proper WSGI server. You can control the number of worker processes with the -w flag, for example gunicorn -w 4 app:app to run four workers.

In a real deployment both processes would be kept alive by a process manager like systemd or supervisord, and a reverse proxy like nginx would sit in front of them to handle HTTPS and route traffic to the right port.""",
        "date": "2024-11-01",
    },
    {
        "id": 11,
        "slug": "image-optimization-done",
        "title": "Image Optimization with next/image",
        "summary": "We replaced the raw img tag on the home page with Next.js Image component. Here is what changed and why it matters.",
        "content": """The home page had a raw img tag loading hello.jpg. The original file is 5784x3856 pixels and around 600KB. Every visitor was downloading that full file regardless of the screen size they were on.

We replaced it with the Image component from next/image. The import is: import Image from 'next/image'

The component takes width and height matching the original image dimensions. These are not the rendered size — they tell Next.js the aspect ratio so it can generate correctly proportioned variants. To make it fill the container width we added style with width 100% and height auto, the same way you would with a regular img tag.

We also added the priority prop. By default Next.js lazy-loads images, which is great for images below the fold. But this image is at the top of the home page — it is visible immediately. The priority prop tells Next.js to preload it so there is no delay on first paint.

What Next.js now does automatically: when a browser requests the page, Next.js checks what size and format to serve. A modern browser on a narrow screen gets a small WebP file. A browser that does not support WebP gets a JPEG. The original file in public/ is never sent directly.

The home page component also lost its "use client" directive. Since the Image component works fine on the server and there is no useState or useEffect in this file, there was no reason to keep it as a client component.

Demo: Let's see it running with throttling for bad 3G
""",
        "date": "2024-10-15",
    },
    {
        "id": 10,
        "slug": "optimizing-images-with-nextjs",
        "title": "Optimizing Images with Next.js",
        "summary": "The home page has a raw img tag. Here is why that is a problem and how Next.js solves it.",
        "content": """The home page currently has a plain HTML img tag pointing to hello.jpg. This works, but the browser downloads the full original file every time — no resizing, no compression, no modern format. On a slow connection or a large image this adds up quickly.

Next.js ships a built-in Image component that handles this automatically. Import it with: import Image from 'next/image'

The component replaces the raw img tag. Instead of src="/hello.jpg" on a plain img, you write the Image component with three required props: src, alt, and a size. You can provide the size either as width and height in pixels, or by adding the fill prop if you want the image to stretch inside a positioned container.

What Next.js does behind the scenes: it resizes the image to the exact dimensions requested, converts it to a modern format like WebP or AVIF if the browser supports it, and serves the result from a built-in image endpoint. The original file in public/ is never sent to the browser directly.

It also adds lazy loading by default, meaning the image is only downloaded when it is about to enter the viewport. For images that are immediately visible on page load, you can add the priority prop to tell Next.js to preload it instead.

One thing to keep in mind: because Next.js generates the optimized versions on demand, the first request for each size is slightly slower. After that the result is cached and served instantly.

To do the optimization, the steps are: remove the raw img tag from app/page.jsx, import Image from next/image, and replace it with the Image component passing src, alt, width, and height.""",
        "date": "2024-10-01",
    },
    {
        "id": 9,
        "slug": "server-components-in-action",
        "title": "Server Components in Action",
        "summary": "We converted the blog list and post pages to server components. Here is exactly what changed.",
        "content": """We just converted app/blog/page.jsx and app/blog/[slug]/page.jsx to server components. The home page was left alone since it has no data fetching.

The first change was removing "use client" from both files. That single line is all that was needed to opt into server components — Next.js treats any component without it as a server component by default.

Both functions became async. This allows using await directly inside the component, which removes the need for useState and useEffect entirely. The fetch call now happens before the component returns its JSX, so the data is always ready when the HTML is generated.

For the blog list page, the current page number used to come from useState. Now it comes from the searchParams prop that Next.js passes automatically to page components. In Next.js 15 and above, searchParams is a Promise, so it needs to be awaited before reading from it.

The pagination buttons were replaced with Link components. Previous and Next are now just links pointing to ?page=2, ?page=3, and so on. This means no onClick handlers, no state — just plain navigation. Server components cannot have event handlers, so this change was necessary, and it turned out to be simpler anyway.

For the post page, the slug used to come from useParams. Now it comes from the params prop, also a Promise in Next.js 15 that needs to be awaited. The entire useEffect, useState, and error state were removed. Checking res.ok after the fetch and returning early is enough to handle a missing post.

The imports got much shorter. Both files now only import Link from next/link. No useState, no useEffect, no useParams.

Questions to think about:

1. Can we use server component with static website?

2. Do server components expose the webpage secrets?
""",
        "date": "2024-09-10",
    },
    {
        "id": 8,
        "slug": "adding-server-components-to-blog",
        "title": "Using Server Components for Blog Pages",
        "summary": "The blog list and individual post pages are good candidates for server components. Here is how to convert them.",
        "content": """Right now our blog pages are client components. They fetch data inside useEffect, which means the page loads first, then the browser makes a request to the Flask API, then the content appears. With server components we can fetch the data before the page is sent to the browser at all.

The pages to convert are app/blog/page.jsx and app/blog/[slug]/page.jsx. The home page has no data fetching so it can stay as-is.

The first thing to do is remove "use client" from both files. Without that directive, Next.js treats the file as a server component by default.

Server components can be async. That means you can use await directly inside the component function, without useEffect or useState. The fetch call moves out of the effect and becomes a simple await at the top of the function body.

For app/blog/page.jsx, the component signature becomes async and you await the fetch call directly. You can also read the page query param from the searchParams prop that Next.js passes to page components automatically — no useState needed for that either.

For app/blog/[slug]/page.jsx, the slug is no longer read with useParams. Instead, Next.js passes it as params.slug in the props. Remove the useParams import and the useEffect, and replace them with a single await fetch using the slug from props.

Because the data is fetched on the server, the loading state is also simpler. Next.js handles the async wait before rendering, so you do not need a loading boolean. If you want a loading UI, you can create a loading.jsx file next to the page and Next.js will show it automatically while the page is being prepared.

Error handling changes slightly too. Instead of catching inside a try/catch in useEffect, you can check the response status directly after the await and return early with a simple not-found message, or use Next.js built-in notFound() function from next/navigation.

One important note: the pagination buttons on /blog use onClick, which is a browser event. Event handlers are not allowed in server components. The fix is to extract just the pagination controls into a small separate file and mark only that file with "use client". The rest of the page stays as a server component. This is the pattern Next.js encourages — push "use client" down to the smallest piece that actually needs it.""",
        "date": "2024-08-05",
    },
    {
        "id": 7,
        "slug": "we-migrated-to-nextjs",
        "title": "We Migrated to Next.js — Here is What We Did",
        "summary": "Step by step: how we converted this blog from Vite React to Next.js, keeping everything client-side.",
        "content": """We just migrated this blog from Vite React to Next.js. Everything is still client-side — no server components yet. Here is exactly what we did.

First, we installed Next.js and removed the packages we no longer needed. We ran npm install next, then npm uninstall vite @vitejs/plugin-react react-router-dom. Next.js has its own router, so react-router-dom is no longer needed.

We updated the scripts in package.json. The dev script changed from "vite" to "next dev", and build changed from "vite build" to "next build". We also added a "start" script for running the production build.

We deleted the files that belong to Vite: index.html, vite.config.js, and the entire src/ folder. Next.js does not need any of those.

We created an app/ directory, which is where Next.js looks for pages. Inside it we created layout.jsx as the root shell — it contains the html and body tags, the navigation, and imports the global CSS. We also created globals.css there to replace the old src/index.css.

For the pages, each route becomes a file. app/page.jsx is the home page. app/blog/page.jsx is the post list. app/blog/[slug]/page.jsx is the individual post — the square brackets tell Next.js that slug is a dynamic segment.

Because we are not using server components yet, every page file starts with "use client" at the top. This tells Next.js to treat the component exactly like a regular React component that runs in the browser.

The data fetching code stayed the same. We still use useEffect and fetch to call the Flask API. The only thing that changed in the page components is that we import Link from next/link instead of react-router-dom, and we use useParams from next/navigation instead of react-router-dom.

Questions to think about:

1. What would change if we removed "use client" from a page?

2. Which pages would actually benefit from becoming server components?

3. Can we run this fully static? (e.g. in GitHub pages)

""",
        "date": "2024-07-01",
    },
    {
        "id": 6,
        "slug": "migrating-react-to-nextjs",
        "title": "Migrating from React Vite to Next.js",
        "summary": "Our blog is currently a pure React app. Here is how we plan to move it to Next.js.",
        "content": """Right now this blog is a pure React app built with Vite. It runs entirely in the browser — there is no server rendering, no file-based routing, and no built-in API layer. Our goal is to migrate it to Next.js.

This is a good learning exercise because Next.js adds a lot of structure on top of plain React. Here are some things to think about as you attempt the migration:

Packages to install: you will need to install next and can remove vite, @vitejs/plugin-react, and the vite.config.js file. Your package.json scripts will also change — instead of "vite" you will run "next dev".

Files to touch: Next.js uses a file-based router. Each file inside the app/ folder becomes a route. You will need to create app/page.jsx for the home page, app/blog/page.jsx for the post list, and app/blog/[slug]/page.jsx for individual posts.

The entry point changes too. Next.js does not have an index.html or main.jsx. The app/layout.jsx file is where you put your global HTML shell and navigation.

Important: for now, mark every component with "use client" at the top of the file. This keeps the behaviour identical to what we have today — everything runs in the browser. Do not use server components yet.

Questions to think about:
1. Does it have server components?
2. Should we convert to use server components?""",
        "date": "2024-06-15",
    },
    {
        "id": 1,
        "slug": "getting-started-with-python",
        "title": "Getting Started with Python",
        "summary": "A beginner's guide to Python programming language.",
        "content": "Python is one of the most popular programming languages today. It has a clean, readable syntax that makes it great for beginners. You can use Python for web development, data science, automation, and much more. Start by installing Python from python.org and writing your first script.",
        "date": "2024-01-10",
    },
    {
        "id": 2,
        "slug": "intro-to-react",
        "title": "Introduction to React",
        "summary": "Learn the basics of building UIs with React.",
        "content": "React is a JavaScript library for building user interfaces. It was created by Facebook and is now maintained by Meta and the open source community. The core idea is to break your UI into reusable components. Each component manages its own state and renders HTML based on that state.",
        "date": "2024-02-05",
    },
    {
        "id": 3,
        "slug": "what-is-rest-api",
        "title": "What is a REST API?",
        "summary": "Understanding REST APIs and how they work.",
        "content": "A REST API (Representational State Transfer) is a way for two systems to communicate over HTTP. The server exposes endpoints like /api/posts and the client sends requests to them. Data is usually exchanged as JSON. REST APIs are stateless, meaning each request contains all the information needed to process it.",
        "date": "2024-03-12",
    },
    {
        "id": 4,
        "slug": "css-flexbox-basics",
        "title": "CSS Flexbox Basics",
        "summary": "A simple guide to CSS Flexbox layout.",
        "content": "Flexbox is a CSS layout model that makes it easy to align and distribute elements. Set display: flex on a container and its children become flex items. Use justify-content to align items on the main axis and align-items for the cross axis. Flexbox is great for navigation bars, card layouts, and centering elements.",
        "date": "2024-04-20",
    },
    {
        "id": 5,
        "slug": "git-for-beginners",
        "title": "Git for Beginners",
        "summary": "Version control basics every developer should know.",
        "content": "Git is a version control system that tracks changes in your code over time. The basic workflow is: make changes, git add to stage them, git commit to save a snapshot, and git push to upload to a remote like GitHub. Branching lets you work on features in isolation before merging them into the main codebase.",
        "date": "2024-05-08",
    },
]


@app.route("/api/posts")
def get_posts():
    time.sleep(1)
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 2))
    start = (page - 1) * per_page
    end = start + per_page
    paginated = posts[start:end]
    total_pages = -(-len(posts) // per_page)  # ceiling division
    return jsonify({
        "posts": paginated,
        "total": len(posts),
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    })


@app.route("/api/posts/<slug>")
def get_post(slug):
    time.sleep(1)
    post = next((p for p in posts if p["slug"] == slug), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
