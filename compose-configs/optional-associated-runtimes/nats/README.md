<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# NATS with JetStream: optional runtime

[NATS](https://nats.io) is a lightweight messaging server. **JetStream** is its persistence
layer: streams (durable, replayable subjects), key-value buckets and object stores. It is here
as an optional runtime for eventing experiments beside Egeria. Nothing is wired to it yet, and
nothing in the quickstart, freshstart or shared-infra stacks starts it or depends on it.

| Piece | What it does |
|---|---|
| `docker-compose.yaml` | One NATS server, container `egeria-optional-nats`, JetStream on, on `egeria_network` |
| `.env.example` | Optional overrides (image, host ports). No secrets. |
| `runtime-volumes/nats/jetstream/` | JetStream's file store (bind mount, git-ignored; created on first start) |

## Ports

| Host | Container | |
|---|---|---|
| `127.0.0.1:4222` | 4222 | Client connections (NATS protocol) |
| `127.0.0.1:8222` | 8222 | HTTP monitoring: `/healthz`, `/varz`, `/jsz`, `/connz` |

Both bind to localhost only, because this config has no client authentication. Containers on
`egeria_network` use `egeria-optional-nats:4222`. Cluster (6222) and leaf-node ports are not
opened. Change the host ports with `NATS_CLIENT_PORT` / `NATS_MONITOR_PORT` in `.env`.

## Start and stop

From this directory. Shared-infra must have run once, so that `egeria_network` exists.

```bash
docker compose up -d --wait     # add --env-file .env if you made one
docker compose ps
curl -s 'http://127.0.0.1:8222/healthz?js-enabled-only=true'   # {"status":"ok"}
docker compose down             # streams stay in runtime-volumes/nats
```

To start empty, stop it and delete `runtime-volumes/nats/jetstream`.

The [NATS CLI](https://github.com/nats-io/natscli) is handy for poking at it, for example from
the `natsio/nats-box` image on the same network:

```bash
docker run --rm -it --network egeria_network natsio/nats-box:latest
nats -s nats://egeria-optional-nats:4222 stream add DEMO --subjects 'demo.>' --defaults
nats -s nats://egeria-optional-nats:4222 pub demo.hello hi
nats -s nats://egeria-optional-nats:4222 stream info DEMO
```

## Connecting from Egeria or Portal code

- **From a container on `egeria_network`** (pyegeria-web, Jupyter, Airflow, Trellis, a Prefect
  worker): `nats://egeria-optional-nats:4222`.
- **From the host** (scripts, a host Prefect worker, tests): `nats://127.0.0.1:4222`.
- **Python** (pyegeria, the Portal's FastAPI handler) would use
  [`nats-py`](https://github.com/nats-io/nats.py), which is asyncio-native, so it fits the
  handler's async routes:

  ```python
  import nats

  nc = await nats.connect(os.environ.get("NATS_URL", "nats://egeria-optional-nats:4222"))
  js = nc.jetstream()
  await js.add_stream(name="EGERIA", subjects=["egeria.>"])
  await js.publish("egeria.element.updated", b'{"guid": "..."}')
  ```

  Read the URL from configuration (for example `NATS_URL`) and treat NATS as absent when it is
  not set: it is optional, and nothing should fail because it is not running.
- **Java** (an Egeria connector, such as an event-bus or integration connector) would use
  [`jnats`](https://github.com/nats-io/nats.java) with the same URL.

Egeria's own event bus stays on Kafka (`egeria-shared-kafka`). This runtime is for new eventing
work only.

## Before exposing it

For anything beyond localhost, add authentication (a config file with users, an nkey or a JWT
operator setup) and TLS, and mount that config instead of using the command-line flags.

License: CC BY 4.0, Copyright Contributors to the ODPi Egeria project.
