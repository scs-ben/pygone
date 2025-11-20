cat > pygone <<'EOF'
#!/bin/sh
T=`mktemp`;tail -n +6 "$0"|xz -d>$T 2>\/dev\/null;chmod +x $T;(sleep 3;rm $T)\&exec $T
EOF

# Append the binary xz payload
cat pygone.xz >> pygone

rm pygone.xz

# Make it executable
chmod +x pygone