echo 'Deploying Server api'

rsync -avrmR \
    --delete-excluded \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ \
    root@5.78.84.141:/root/makinginvest-python-api

ssh root@5.78.84.141 << EOF
    cd makinginvest-python-api/ && \
    docker-compose up -d --build makinginvest-python-api
EOF

echo 'Deployed Server api'
