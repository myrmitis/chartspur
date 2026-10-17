"""Offline contracts for the actual Worker; discovered by the existing CI job.

Node's fetch is replaced before importing the Worker. No network, credentials,
chart refresh, payment provider, or Cloudflare deployment is used.
"""
import json
from pathlib import Path
import shutil
import subprocess
import unittest
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://chartspur.com"
PAGES = "https://myrmitis.github.io/chartspur"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
HARNESS = r"""
import { readFileSync } from 'node:fs';
const input = JSON.parse(readFileSync(0, 'utf8'));
const calls = [];
globalThis.fetch = async (url, options) => {
  calls.push({url: String(url), options});
  const fixture = input.upstream;
  if (!fixture) throw new Error('Unexpected upstream request');
  return new Response(options.method === 'HEAD' ? null : (fixture.body ?? 'upstream'), {
    status: fixture.status ?? 200, headers: fixture.headers ?? {'content-type': 'text/html'},
  });
};
const code = readFileSync('edge/worker.js').toString('base64');
const {default: worker} = await import('data:text/javascript;base64,' + code);
const response = await worker.fetch(new Request(input.url, {method: input.method ?? 'GET'}));
console.log(JSON.stringify({status: response.status, headers: Object.fromEntries(response.headers),
  body: await response.text(), calls}));
"""


class EdgeSEOTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("node"):
            raise RuntimeError("Node 22+ is required; the existing CI job installs it")

    def request(self, path, method="GET", upstream=None, host=ORIGIN):
        result = subprocess.run(
            ["node", "--input-type=module", "-e", HARNESS], cwd=ROOT,
            input=json.dumps({"url": host + path, "method": method, "upstream": upstream}),
            text=True, capture_output=True, timeout=10, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_sitemap_is_valid_xml_with_only_approved_canonicals(self):
        result = self.request("/sitemap.xml")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["headers"]["content-type"], "application/xml; charset=utf-8")
        root = ET.fromstring(result["body"])
        self.assertEqual(root.tag, NS + "urlset")
        urls = [item.findtext(NS + "loc") for item in root]
        self.assertEqual(urls, [ORIGIN + "/", ORIGIN + "/brief.html"])
        self.assertEqual(len(urls), len(set(urls)))
        for url in urls:
            parsed = urlsplit(url)
            self.assertEqual((parsed.scheme, parsed.netloc), ("https", "chartspur.com"))
            self.assertFalse(parsed.query or parsed.fragment or parsed.username or parsed.password)
        self.assertFalse(root.findall(".//" + NS + "lastmod"))
        self.assertFalse(result["calls"])

    def test_robots_declares_map_without_overriding_managed_policy(self):
        result = self.request("/robots.txt")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["headers"]["content-type"], "text/plain; charset=utf-8")
        directives = [line for line in result["body"].splitlines() if line and not line.startswith("#")]
        self.assertEqual(directives, ["Sitemap: " + ORIGIN + "/sitemap.xml"])
        self.assertFalse(result["calls"])

    def test_managed_training_restrictions_survive_composition(self):
        # A composition fixture, not a claim about the deployed Cloudflare zone.
        managed = "User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n\n"
        parser = RobotFileParser()
        parser.parse((managed + self.request("/robots.txt")["body"]).splitlines())
        for agent in ("Googlebot", "Bingbot", "OAI-SearchBot"):
            self.assertTrue(parser.can_fetch(agent, ORIGIN + "/brief.html"))
        self.assertFalse(parser.can_fetch("GPTBot", ORIGIN + "/"))

    def test_head_matches_get_headers_and_has_no_body(self):
        for path in ("/robots.txt", "/sitemap.xml"):
            with self.subTest(path=path):
                get = self.request(path)
                head = self.request(path, "HEAD")
                self.assertEqual(head["status"], 200)
                self.assertEqual(head["headers"], get["headers"])
                self.assertEqual(head["body"], "")
                self.assertFalse(head["calls"])

    def test_query_and_fragment_never_enter_discovery_output(self):
        for path in ("/robots.txt", "/sitemap.xml"):
            with self.subTest(path=path):
                self.assertEqual(self.request(path + "?probe=synthetic#fragment")["body"],
                                 self.request(path)["body"])

    def test_discovery_responses_keep_bounded_cache_and_security_headers(self):
        for path in ("/robots.txt", "/sitemap.xml"):
            with self.subTest(path=path):
                headers = self.request(path)["headers"]
                self.assertEqual(headers["cache-control"], "public, max-age=300")
                self.assertEqual(headers["x-content-type-options"], "nosniff")
                self.assertEqual(headers["referrer-policy"], "strict-origin-when-cross-origin")
                self.assertNotIn("set-cookie", headers)
                self.assertNotIn("last-modified", headers)

    def test_nonread_methods_remain_rejected(self):
        for path in ("/robots.txt", "/sitemap.xml", "/brief.html"):
            for method in ("POST", "PUT", "DELETE", "OPTIONS"):
                with self.subTest(path=path, method=method):
                    result = self.request(path, method)
                    self.assertEqual(result["status"], 405)
                    self.assertEqual(result["headers"]["allow"], "GET, HEAD")
                    self.assertFalse(result["calls"])

    def test_www_redirect_keeps_existing_path_and_query_behavior(self):
        for path in ("/", "/robots.txt", "/sitemap.xml", "/brief.html?probe=synthetic"):
            with self.subTest(path=path):
                result = self.request(path, host="https://www.chartspur.com")
                self.assertEqual(result["status"], 301)
                self.assertEqual(result["headers"]["location"], ORIGIN + path)
                self.assertFalse(result["calls"])

    def test_aliases_redirect_once_before_proxy_or_discovery_handling(self):
        for host in ("http://chartspur.com", "http://www.chartspur.com", "https://www.chartspur.com"):
            for path in ("/", "/brief.html", "/robots.txt", "/sitemap.xml"):
                for method in ("GET", "HEAD"):
                    with self.subTest(host=host, path=path, method=method):
                        result = self.request(path, method, host=host)
                        self.assertEqual(result["status"], 301)
                        self.assertEqual(result["headers"]["location"], ORIGIN + path)
                        self.assertEqual(result["body"], "")
                        self.assertFalse(result["calls"])
                        target = urlsplit(result["headers"]["location"])
                        final = self.request(target.path, method, {"body": "public page"},
                                             host=f"{target.scheme}://{target.netloc}")
                        self.assertEqual(final["status"], 200)
                        self.assertNotIn("location", final["headers"])
                        discovery = path in ("/robots.txt", "/sitemap.xml")
                        self.assertEqual(len(final["calls"]), 0 if discovery else 1)
                        if method == "HEAD":
                            self.assertEqual(final["body"], "")

    def test_redirects_preserve_encoded_paths_and_queries(self):
        query = "?genre=Photo%20%26%20Video&tag=a&tag=b&empty=&literal=a+b&encoded=%2B%252F"
        for host in ("http://chartspur.com", "http://www.chartspur.com", "https://www.chartspur.com"):
            for path in ("/", "/brief.html", "/robots.txt", "/sitemap.xml", "/nested/a%2Fb%20c"):
                with self.subTest(host=host, path=path):
                    result = self.request(path + query, host=host)
                    self.assertEqual(result["status"], 301)
                    self.assertEqual(result["headers"]["location"], ORIGIN + path + query)
                    self.assertFalse(result["calls"])

    def test_https_apex_proxy_preserves_query_and_external_payment_redirect(self):
        path = "/brief.html?genre=Photo%20%26%20Video&tag=a&tag=b&empty="
        # Inert upstream fixture: never contact Stripe or initiate checkout.
        payment = "https://buy.stripe.com/test_synthetic"
        result = self.request(path, upstream={"status": 302, "headers": {"location": payment}})
        self.assertEqual(result["status"], 302)
        self.assertEqual(result["headers"]["location"], payment)
        self.assertEqual(len(result["calls"]), 1)
        self.assertEqual(result["calls"][0]["url"], PAGES + path)
        self.assertEqual(result["calls"][0]["options"]["redirect"], "manual")

    def test_http_ports_redirect_to_default_https_apex(self):
        path = "/brief.html?genre=Photo%20%26%20Video"
        for host in ("chartspur.com", "www.chartspur.com"):
            for port in (80, 8080, 8880, 2052, 2082, 2086, 2095):
                with self.subTest(host=host, port=port):
                    result = self.request(path, host=f"http://{host}:{port}")
                    self.assertEqual(result["status"], 301)
                    self.assertEqual(result["headers"]["location"], ORIGIN + path)
                    self.assertFalse(result["calls"])

    def test_https_nondefault_ports_keep_existing_behavior(self):
        apex = self.request("/brief.html", host=ORIGIN + ":8443", upstream={"body": "public page"})
        self.assertEqual(apex["status"], 200)
        self.assertNotIn("location", apex["headers"])
        self.assertEqual(apex["calls"][0]["url"], PAGES + "/brief.html")
        alias = self.request("/brief.html", host="https://www.chartspur.com:8443")
        self.assertEqual(alias["status"], 301)
        self.assertEqual(alias["headers"]["location"], ORIGIN + ":8443/brief.html")
        self.assertFalse(alias["calls"])

    def test_existing_public_pages_and_data_still_proxy_to_pages(self):
        for path in ("/", "/brief.html", "/data/live.json", "/app.js"):
            with self.subTest(path=path):
                result = self.request(path, upstream={"body": "unchanged fixture"})
                self.assertEqual(result["body"], "unchanged fixture")
                self.assertEqual(result["calls"][0]["url"], PAGES + path)
                options = result["calls"][0]["options"]
                self.assertEqual(options["method"], "GET")
                self.assertEqual(options["redirect"], "manual")
                self.assertEqual(options["cf"], {"cacheEverything": True, "cacheTtl": 300})

    def test_only_exact_discovery_paths_are_intercepted(self):
        for path in ("/nested/sitemap.xml", "/robots.txt/", "/SITEMAP.XML", "/api/sitemap.xml"):
            with self.subTest(path=path):
                result = self.request(path, upstream={"status": 404, "body": "not found"})
                self.assertEqual(result["status"], 404)
                self.assertEqual(result["body"], "not found")
                self.assertEqual(len(result["calls"]), 1)

    def test_upstream_head_status_and_headers_are_preserved(self):
        result = self.request("/brief.html", "HEAD", {"status": 200, "headers": {"etag": '"fixture"'}})
        self.assertEqual(result["body"], "")
        self.assertEqual(result["headers"]["etag"], '"fixture"')
        self.assertEqual(result["calls"][0]["options"]["method"], "HEAD")

    def test_upstream_redirects_keep_existing_custom_domain_rewrite(self):
        result = self.request("/docs", upstream={"status": 301, "headers": {"location": PAGES + "/docs/"}})
        self.assertEqual(result["status"], 301)
        self.assertEqual(result["headers"]["location"], ORIGIN + "/docs/")

    def test_upstream_error_does_not_become_a_success(self):
        result = self.request("/missing", upstream={"status": 503, "body": "unavailable"})
        self.assertEqual(result["status"], 503)
        self.assertEqual(result["body"], "unavailable")


if __name__ == "__main__":
    unittest.main()
