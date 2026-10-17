// Serves the GitHub Pages build at chartspur.com. Pages stays the build and deploy path (pages.yml).
const ORIGIN = "https://myrmitis.github.io/chartspur";
const HOST = "chartspur.com";

// Only the approved public homepage and free sample brief belong in this map.
// Omit lastmod: a Worker deploy is not evidence that either page changed.
const SITEMAP = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://${HOST}/</loc></url>
  <url><loc>https://${HOST}/brief.html</loc></url>
</urlset>
`;
// Cloudflare prepends its managed crawler policy. Do not override it with Allow
// rules or copy a policy snapshot that could become stale.
const ROBOTS = `# Crawler restrictions remain managed by Cloudflare.
Sitemap: https://${HOST}/sitemap.xml
`;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.protocol !== "https:" || url.hostname !== HOST) {
      url.protocol = "https:";
      url.hostname = HOST;
      return Response.redirect(url.toString(), 301);
    }
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", { status: 405, headers: { Allow: "GET, HEAD" } });
    }
    // These deployment-independent discovery files do not contact Pages or
    // reflect request parameters. All other routing and responses stay intact.
    if (url.pathname === "/robots.txt" || url.pathname === "/sitemap.xml") {
      const sitemap = url.pathname === "/sitemap.xml";
      return new Response(request.method === "HEAD" ? null : sitemap ? SITEMAP : ROBOTS, {
        headers: {
          "Content-Type": sitemap ? "application/xml; charset=utf-8" : "text/plain; charset=utf-8",
          "Cache-Control": "public, max-age=300",
          "X-Content-Type-Options": "nosniff",
          "Referrer-Policy": "strict-origin-when-cross-origin",
        },
      });
    }
    const upstream = await fetch(ORIGIN + url.pathname + url.search, {
      method: request.method,
      redirect: "manual",
      cf: { cacheEverything: true, cacheTtl: 300 },
    });
    const headers = new Headers(upstream.headers);
    // Pages redirects /dir to /chartspur/dir/ on its own host; keep the visitor on chartspur.com.
    const location = headers.get("Location");
    if (location?.startsWith(ORIGIN)) {
      headers.set("Location", `https://${HOST}${location.slice(ORIGIN.length) || "/"}`);
    }
    headers.set("X-Content-Type-Options", "nosniff");
    headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
    return new Response(upstream.body, { status: upstream.status, headers });
  },
};
