echo 'Deploying Traefik'

rsync -avrmR --delete --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@5.78.84.141:/root/makinginvest-traefik

ssh root@5.78.84.141 << EOF
    docker network create traefik-network
    cd makinginvest-traefik/ && docker-compose up -d
EOF

echo 'Deployed Traefik'
