const proxy = require('http-proxy-middleware');

module.exports = function(app) {
  // Pour Docker: utilise 'http://api:5000' (nom du service dans docker-compose)
  app.use(
    '/api',
    proxy({
      target: 'http://api:5000',
      changeOrigin: true,
      secure: false
    })
  );
};

