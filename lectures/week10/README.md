- do not use sqlite
- use postgres, mysql, mariadb, oracle, ...
  replace DB_URI = "sqlite://storage.db" 
  this DB_URI = "postgres://username:password@127.0.0.1:5678/mydatabase"
  this DB_URI = "google:datastore"
- use static files and configure web server to serve static files
- minimize number of DB queries
- make simple DB queries
- use cache (Kafka)
- load balancer (haproxy, nginx)
- kubernetes

- deploy in cloud
  - pythonanywhere
  - DigitalOcean - AWS - GKE(Google)
  - GAE - Google
