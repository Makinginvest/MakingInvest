echo 'Deploying Traefik'

rsync -avrmR --delete --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@49.13.84.137:/root/stockwatchalert-traefik

ssh root@49.13.84.137 << EOF
    docker network create traefik-network
    cd stockwatchalert-traefik/ && docker-compose up -d
EOF

echo 'Deployed Traefik'
