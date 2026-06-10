cat > ./dist/pygone <<'EOF'
#!/bin/sh
t=/tmp/p$$;tail -n+3 $0|xz -d>$t;pypy3 $t;rm $t
EOF

# Append the binary xz payload
cat ./dist/pygone.xz >> ./dist/pygone

rm ./dist/pygone.xz

# Make it executable
chmod +x ./dist/pygone