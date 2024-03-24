echo 'Deploying Server Engines'

rsync -avrmR \
    --delete-excluded \
    --exclude='_project/data/backtest/*' \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ root@188.34.177.82:/root/makinginvest-python-engines-worker

ssh root@188.34.177.82 << EOF
    cd makinginvest-python-engines-worker/ && docker-compose up -d --build makinginvest-python-engines-worker
EOF

echo 'Deployed Server Engines'
