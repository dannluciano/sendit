# SendIT IDE

A SendIT editor and shell


## Deployment

To run this project exec:

```bash
$ docker compose up --build -d && docker compose logs -f
```

or

```bash
$ docker compose watch
```

and on other term tab

```bash
$ docker compose logs -f
```

## To test docker socket

```bash
curl --unix-socket /var/run/docker.sock -H "Content-Type: application/json" http://localhost/info
curl --unix-socket /run/docker.sock -H "Content-Type: application/json" http://localhost/info
```

## Authors

- [@dannluciano](https://www.github.com/dannluciano)
