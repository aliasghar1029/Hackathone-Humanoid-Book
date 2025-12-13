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
              logLevel: 'debug',
              onProxyReq: (proxyReq, req, res) => {
                console.log(`Proxying ${req.method} ${req.url} to ${'http://127.0.0.1:8000'}`);
              },
              onProxyRes: (proxyRes, req, res) => {
                console.log(`Received response from ${req.url} with status ${proxyRes.statusCode}`);
              }
            },
          ],
        },
      };
    },
  };
}

module.exports = proxyPlugin;