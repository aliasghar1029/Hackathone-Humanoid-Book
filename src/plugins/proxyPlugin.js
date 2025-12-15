// @ts-check

/**
 * @param {import('@docusaurus/types').LoadContext} context
 * @returns {import('@docusaurus/types').Plugin}
 */
function proxyPlugin(context, options) {
  return {
    name: 'docusaurus-proxy-plugin',
    configureWebpack(config, isServer, utils) {
      return {
        devServer: {
          proxy: [
            {
              context: ['/api', '/query', '/ingest', '/health'],
              target: 'http://127.0.0.1:8000',
              changeOrigin: true,
              logLevel: 'silent', // Reduce logging to avoid console noise
              onProxyReq: (proxyReq, req, res) => {
                // Optional: Add custom logic here if needed
              },
              onProxyRes: (proxyRes, req, res) => {
                // Optional: Add custom logic here if needed
              },
              onError: (err, req, res) => {
                // Handle proxy errors gracefully - this prevents the console error
                console.warn(`Backend not available: ${req.url}. Using client-side fallback.`);
              }
            },
          ],
        },
      };
    },
  };
}

module.exports = proxyPlugin;