<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# OpenFGA: optional runtime

[OpenFGA](https://openfga.dev) is a fine-grained authorization server based on Google's
Zanzibar: you write an authorization model (types and relations), store relationship tuples
(`user:erin` is `viewer` of `glossary:clinical-trials`), and ask it questions (`Check`,
`ListObjects`). It is here as an optional runtime for fine-grained authorization experiments
beside Egeria. Nothing is wired to it yet, and nothing in the quickstart, freshstart or
shared-infra stacks starts it or depends on it.

| Piece | What it does |
|---|---|
| `docker-compose.yaml` | `openfga-migrate` (runs `openfga migrate`, then exits) and `openfga` (runs only after the migrate step succeeds), on `egeria_network` |
| `.env.example` | Datastore password, host ports, playground and API auth switches |

## Ports

| Host | Container | |
|---|---|---|
| `127.0.0.1:8090` | 8080 | HTTP API (`/healthz`, `/stores`, …) |
| `127.0.0.1:8091` | 8081 | gRPC API |
| `127.0.0.1:3030` | 3000 | Playground, only when `OPENFGA_PLAYGROUND_ENABLED=true` |

The host ports are moved off OpenFGA's own 8080, 8081 and 3000, which Airflow, the Spark
sandbox and Marquez use on this repo's hosts. Containers on `egeria_network` use the container
ports: `http://egeria-optional-openfga:8080` and `egeria-optional-openfga:8081`. All three bind to
localhost only. Change them with `OPENFGA_HTTP_PORT`, `OPENFGA_GRPC_PORT` and
`OPENFGA_PLAYGROUND_PORT`.

## Datastore

OpenFGA keeps its models and tuples in an `openfga` database on shared-infra's
`egeria-shared-postgres` (port 5442), owned by an `openfga_admin` role, the same way Prefect and
TestGen get theirs. The `migrate` step creates and upgrades OpenFGA's tables in that database on
every start, so its schema always matches the image.

This config does not create the database or role, and no shared-infra script does either, so
the shared Postgres is unchanged until you opt in. Run this once. **It is a write to the shared
Postgres, so tell the other sessions first** (a peer round):

```bash
cp .env.example .env      # then set OPENFGA_DB_PASSWORD (openssl rand -hex 24)
docker exec -i egeria-shared-postgres psql -U postgres -p 5442 -v ON_ERROR_STOP=1 \
     -v fga_password="$(grep '^OPENFGA_DB_PASSWORD=' .env | cut -d= -f2-)" <<'EOSQL'
SELECT NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'openfga_admin') AS need_role \gset
\if :need_role
    CREATE ROLE openfga_admin WITH LOGIN;
\endif
ALTER ROLE openfga_admin WITH PASSWORD :'fga_password';
SELECT 'CREATE DATABASE openfga OWNER openfga_admin'
 WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'openfga') \gexec
EOSQL
```

It is idempotent; re-run it to change the password. To remove OpenFGA's data entirely:
`DROP DATABASE openfga; DROP ROLE openfga_admin;` (again, tell the other sessions first).

To use a different Postgres, set `OPENFGA_DB_HOST`, `OPENFGA_DB_PORT`, `OPENFGA_DB_NAME` and
`OPENFGA_DB_SSLMODE` in `.env`.

## Start and stop

From this directory, with shared-infra up and the datastore created:

```bash
docker compose --env-file .env up -d --wait
docker compose --env-file .env ps -a          # openfga-migrate shows "Exited (0)"
curl -s http://127.0.0.1:8090/healthz         # {"status":"SERVING"}
docker compose --env-file .env down           # data stays in the openfga database
```

If `openfga` does not start, read the migrate step first:
`docker logs egeria-optional-openfga-migrate`.

## Playground

The playground is off by default; upstream has deprecated the built-in one. Set
`OPENFGA_PLAYGROUND_ENABLED=true` in `.env` and restart to serve it at
`http://127.0.0.1:3030/playground`. That page only frames the hosted
`https://play.fga.dev` sandbox, pointed at the API on `127.0.0.1:8080`, which is the container's
port, not this config's host port. So open the sandbox at the right port directly instead
(it works whether or not the built-in playground is on):

```
https://play.fga.dev/sandbox/?fga_api_host=127.0.0.1%3a8090&fga_api_scheme=http
```

The page comes from openfga.dev, but your browser makes the API calls to your local server, so
the models and tuples stay on this machine.

## API authentication

`OPENFGA_AUTHN_METHOD=none` by default, which is acceptable only because the ports are
localhost-only and the containers on `egeria_network` are ours. To require a key, set
`OPENFGA_AUTHN_METHOD=preshared` and `OPENFGA_AUTHN_PRESHARED_KEYS` (comma-separated,
`openssl rand -hex 32` each), and send `Authorization: Bearer <key>`. The playground does not
work with keys.

## Connecting from Egeria or Portal code

- **From a container on `egeria_network`** (pyegeria-web, Jupyter, Trellis):
  `http://egeria-optional-openfga:8080` (HTTP) or `egeria-optional-openfga:8081` (gRPC).
- **From the host**: `http://127.0.0.1:8090`.
- **Python** (pyegeria, the Portal's FastAPI handler) would use the
  [`openfga-sdk`](https://github.com/openfga/python-sdk) package, whose `OpenFgaClient` is
  async, so it fits the handler's async routes:

  ```python
  from openfga_sdk import ClientConfiguration, OpenFgaClient
  from openfga_sdk.client.models import ClientCheckRequest

  cfg = ClientConfiguration(
      api_url=os.environ["OPENFGA_API_URL"],        # http://egeria-optional-openfga:8080
      store_id=os.environ["OPENFGA_STORE_ID"],
  )
  async with OpenFgaClient(cfg) as fga:
      allowed = (await fga.check(ClientCheckRequest(
          user="user:erinoverview", relation="viewer", object="glossary:clinical-trials"))).allowed
  ```

  Create the store (`POST /stores`) and write the model once, then keep the store ID (and the
  model ID, to pin it) in configuration. Treat OpenFGA as absent when `OPENFGA_API_URL` is not
  set: it is optional, and nothing should fail because it is not running.
- **Java** (an Egeria platform security connector or a metadata security connector) would use
  [`openfga-java-sdk`](https://github.com/openfga/java-sdk) against the same URL.

Egeria's own access control (governance zones, platform and server security connectors) is
unchanged. This runtime is for new fine-grained authorization work only.

License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
