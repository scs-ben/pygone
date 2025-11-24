cat > ./dist/pygone <<'EOF'
#!/bin/sh
t=$(mktemp);tail -n+3 $0 | xz -d > $t;chmod +x $t;(sleep 3; rm $t)&exec $t
EOF

# Append the binary xz payload
cat ./dist/pygone.xz >> ./dist/pygone

rm ./dist/pygone.xz

# Make it executable
chmod +x ./dist/pygone