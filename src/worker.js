export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Serve static assets via Cloudflare Workers Assets
    let response = await env.ASSETS.fetch(request);
    
    // If not found and not a direct file request with extension, serve SPA index.html
    if (response.status === 404 && !url.pathname.split("/").pop().includes(".")) {
      const spaRequest = new Request(new URL("/", request.url), request);
      response = await env.ASSETS.fetch(spaRequest);
    }
    
    return response;
  }
};
