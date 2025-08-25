const http = require('http');
const fs = require('fs');
const path = require('path');

http.createServer(function (req, res) {
  // Tentukan path file HTML
  const filePath = path.join(__dirname, 'login.html');

  // Baca file html
  fs.readFile(filePath, function (err, data) {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Error loading page');
    } else {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    }
  });

}).listen(8080, () => {
  console.log("Server running at http://localhost:8080/");
});
