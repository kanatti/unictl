# Setting up Elasticsearch for Local Testing

## Using Docker

1. Pull the Elasticsearch Docker image:
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.8.23
```

2. Run Elasticsearch in a Docker container:
```bash
docker run -d --name elasticsearch \
    -p 9200:9200 -p 9300:9300 \
    -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.8.23
```

3. Verify that Elasticsearch is running:
```bash
curl http://localhost:9200/_cluster/health
```

## Bootstrapping Elasticsearch

Use the following script:

```bash
./dev/bootstrap-es.sh
```

This script will create three indices (users, products, and orders) with appropriate mappings and populate them with sample data.

## Verifying the Setup

After running the bootstrap script, you can verify the setup by querying Elasticsearch:

List all indices:
```bash
curl -X GET "localhost:9200/_cat/indices?v"
```
