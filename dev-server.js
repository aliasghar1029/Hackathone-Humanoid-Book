const path = require('path');
const express = require('express');
const proxy = require('http-proxy-middleware').createProxyMiddleware;
const chalk = require('chalk');
const chokidar = require('chokidar');
const fs = require('fs-extra');
const getDocusaurusConfig = require('@docusaurus/core/lib/commands/utils').getDocusaurusConfig;
const { build } = require('@docusaurus/core');

const config = getDocusaurusConfig(path.resolve(__dirname));

const app = express();

// Proxy API requests to the backend
app.use(
  ['/api', '/query', '/ingest'],
  proxy({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    logLevel: 'debug',
  })
);

// Serve static files
app.use(express.static(path.join(__dirname, 'build')));

// Fallback to index.html for client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(chalk.green(`Server running on port ${PORT}`));
  console.log(chalk.blue(`Proxying API requests to http://127.0.0.1:8000`));
});