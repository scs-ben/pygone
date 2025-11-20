cat > pygone <<'EOF'
#!/bin/sh
t=$(mktemp);tail -n+3 $0 | xz -d > $t;chmod +x $t;(sleep 3; rm $t)&exec $t
EOF

# Append the binary xz payload
cat pygone.xz >> pygone

rm pygone.xz

# Make it executable
chmod +x pygone