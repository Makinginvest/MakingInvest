echo 'Deploying Traefik'

rsync -avrmR --delete --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@188.34.177.82:/root/stockwatchalert-traefik

ssh root@188.34.177.82 << EOF
    docker network create traefik-network
    cd stockwatchalert-traefik/ && docker-compose up -d
EOF

echo 'Deployed Traefik'
