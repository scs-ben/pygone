cat > ./dist/pygone <<'EOF'
#!/bin/sh
tail -n+3 $0|xz -d>_$$;pypy3 _$$;rm _$$
EOF

# Append the binary xz payload
cat ./dist/pygone.xz >> ./dist/pygone

rm ./dist/pygone.xz

# Make it executable
chmod +x ./dist/pygone