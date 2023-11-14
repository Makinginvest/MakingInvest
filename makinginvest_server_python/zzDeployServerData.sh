echo 'Deploying Server data'

rsync -avrmR \
    --delete-excluded \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ root@5.78.84.141:/root/makinginvest-python-data

ssh root@5.78.84.141 << EOF
    cd makinginvest-python-data/ && docker-compose up -d --build makinginvest-python-data
EOF

echo 'Deployed Server data'
