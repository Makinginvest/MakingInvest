echo 'Deploying Server websocket'

rsync -avrmR \
    --delete-excluded \
    --exclude='__venv/*' \
    --exclude='_project/data/backtest/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ root@188.34.177.82:/root/makinginvest-python-api-websocket

ssh root@188.34.177.82 << EOF
    cd makinginvest-python-api-websocket/ && docker-compose up -d --build makinginvest-python-api-websocket
EOF

echo 'Deployed Server websocket'
