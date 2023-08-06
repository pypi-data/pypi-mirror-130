compile.sh
docker-compose -f docker-compose-proxy.yml down
docker-compose -f docker-compose-proxy.yml up -d
PORT=${PORT:-8080} python index.pypython index.py