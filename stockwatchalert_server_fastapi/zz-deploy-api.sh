echo 'Deploying Server api'

rsync -avrmR \
    --delete-excluded \
    --exclude='_project/data/*' \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ \
    root@188.34.177.82:/root/makinginvest-python-api

ssh root@188.34.177.82 << EOF
    cd makinginvest-python-api/ && \
    docker-compose up -d --build makinginvest-python-api
EOF

echo 'Deployed Server api'
