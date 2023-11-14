echo 'Deploying Server websocket'

rsync -avrmR \
    --delete-excluded \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ root@5.78.84.141:/root/makinginvest-python-websocket

ssh root@5.78.84.141 << EOF
    cd makinginvest-python-websocket/ && docker-compose up -d --build makinginvest-python-websocket
EOF

echo 'Deployed Server websocket'
