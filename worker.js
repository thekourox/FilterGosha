/**
 * Cloudflare Worker Reverse Proxy for X4G Panel (VLESS + WebSocket + TLS)
 * ========================================================================
 * Author: Kourosh
 * Purpose: Transparently proxies HTTP & WebSocket traffic from Cloudflare Edge
 *          to a Railway backend (e.g. x4g-backend.up.railway.app) to bypass
 *          DPI throttling in Iran (Irancell / RighTel).
 *
 * HOW TO DEPLOY:
 * --------------
 * Option A: Cloudflare Dashboard
 * 1. Go to Cloudflare Dashboard -> Workers & Pages -> Create Worker.
 * 2. Replace all code with this file's content.
 * 3. Update BACKEND_HOST below or add Environment Variable BACKEND_HOST in Worker Settings.
 * 4. Click "Save and Deploy".
 * 5. (Optional) Under Triggers -> Add Custom Domain (e.g., worker.mydomain.com).
 *
 * Option B: Wrangler CLI
 * 1. npx wrangler deploy worker.js --name x4g-worker-proxy
 */

// Default Railway backend domain (Fallback if env.BACKEND_HOST is not set)
const DEFAULT_BACKEND_HOST = "x4g-backend.up.railway.app";

export default {
  async fetch(request, env, ctx) {
    try {
      // 1. Determine target backend hostname
      const backendHost = env.BACKEND_HOST || DEFAULT_BACKEND_HOST;

      // 2. Clone request URL and rewrite hostname to Railway domain
      const url = new URL(request.url);
      url.hostname = backendHost;
      url.protocol = "https:"; // Ensure HTTPS to Railway

      // 3. Prepare headers for transparent reverse proxying
      const headers = new Headers(request.headers);
      headers.set("Host", backendHost);
      headers.set("X-Forwarded-Host", request.headers.get("Host") || url.hostname);
      headers.set("X-Forwarded-Proto", "https");

      // Preserve real client IP
      const clientIp = request.headers.get("CF-Connecting-IP");
      if (clientIp) {
        headers.set("X-Real-IP", clientIp);
        const existingFwd = request.headers.get("X-Forwarded-For");
        headers.set("X-Forwarded-For", existingFwd ? `${existingFwd}, ${clientIp}` : clientIp);
      }

      // 4. Construct outgoing fetch options
      const fetchInit = {
        method: request.method,
        headers: headers,
        redirect: "manual",
      };

      // Attach request body for POST/PUT/PATCH or WebSocket handshake
      if (request.method !== "GET" && request.method !== "HEAD") {
        fetchInit.body = request.body;
      }

      // 5. Proxy request to Railway backend
      // Cloudflare Workers fetch() natively proxies WebSocket upgrade requests when Upgrade header is present
      const response = await fetch(url.toString(), fetchInit);

      // 6. Return backend response with CORS headers
      const responseHeaders = new Headers(response.headers);
      responseHeaders.set("Access-Control-Allow-Origin", "*");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders,
      });
    } catch (err) {
      return new Response(`Cloudflare Worker Proxy Error: ${err.message}`, {
        status: 502,
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }
  },
};
