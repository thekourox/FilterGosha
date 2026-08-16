/**
 * X4G Panel - Cloudflare Worker Reverse Proxy (Anti-DPI / WebSocket Bypass)
 * 
 * Instructions:
 * 1. Go to Cloudflare Dashboard -> Workers & Pages -> Create Worker.
 * 2. Paste this code into the editor.
 * 3. Replace 'RAILWAY_BACKEND' with your actual Railway domain (e.g., 'kouroshnet.vazirigoldgallery.ir').
 * 4. Save and Deploy.
 * 5. Add Custom Domain (e.g., 'gold.vazirigoldgallery.ir') under Worker Settings -> Triggers.
 */

const RAILWAY_BACKEND = "kouroshnet.vazirigoldgallery.ir";

export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      
      // Rewrite destination hostname to Railway server
      url.hostname = RAILWAY_BACKEND;
      url.protocol = "https:";
      url.port = "443";

      // Duplicate headers and set appropriate Host and X-Forwarded headers
      const newHeaders = new Headers(request.headers);
      newHeaders.set("Host", RAILWAY_BACKEND);
      newHeaders.set("X-Forwarded-Host", request.headers.get("Host") || url.hostname);
      newHeaders.set("X-Forwarded-Proto", "https");

      const clientIp = request.headers.get("CF-Connecting-IP");
      if (clientIp) {
        newHeaders.set("X-Real-IP", clientIp);
        newHeaders.set("CF-Connecting-IP", clientIp);
        const existingFwd = request.headers.get("X-Forwarded-For");
        newHeaders.set("X-Forwarded-For", existingFwd ? `${existingFwd}, ${clientIp}` : clientIp);
      }

      // Check if WebSocket upgrade request
      const isWebSocket = request.headers.get("Upgrade")?.toLowerCase() === "websocket";

      if (isWebSocket) {
        return fetch(url.toString(), {
          method: request.method,
          headers: newHeaders,
          body: request.body,
          redirect: "manual"
        });
      }

      // Standard HTTP fetch
      const response = await fetch(url.toString(), {
        method: request.method,
        headers: newHeaders,
        body: request.method !== "GET" && request.method !== "HEAD" ? request.body : null,
        redirect: "manual"
      });

      // Wrap response headers for CORS compatibility
      const responseHeaders = new Headers(response.headers);
      responseHeaders.set("Access-Control-Allow-Origin", "*");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders
      });
    } catch (err) {
      return new Response(`X4G Worker Proxy Error: ${err.message}`, { status: 502 });
    }
  }
};
