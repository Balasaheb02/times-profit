#!/bin/bash

echo "🔧 PostgreSQL Remote Access Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Run these commands on your VPS to enable remote access:"
echo ""

echo "1. 📝 Edit PostgreSQL configuration:"
echo "   sudo nano /etc/postgresql/*/main/postgresql.conf"
echo ""
echo "   Find this line:"
echo "   #listen_addresses = 'localhost'"
echo ""
echo "   Change it to:"
echo "   listen_addresses = '*'"
echo ""

echo "2. 🔐 Edit PostgreSQL client authentication:"
echo "   sudo nano /etc/postgresql/*/main/pg_hba.conf"
echo ""
echo "   Add this line at the end:"
echo "   host    all             all             0.0.0.0/0               md5"
echo ""

echo "3. 🔄 Restart PostgreSQL:"
echo "   sudo systemctl restart postgresql"
echo ""

echo "4. 🔥 Open firewall port:"
echo "   sudo ufw allow 5432"
echo ""

echo "5. ✅ Test configuration:"
echo "   sudo netstat -tlnp | grep 5432"
echo "   # Should show: 0.0.0.0:5432"
echo ""

echo "6. 🧪 Test remote connection:"
echo "   psql -h YOUR_VPS_IP -U newsuser -d newsdb"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  SECURITY NOTE: This opens PostgreSQL to the internet."
echo "🔒 For production, restrict to specific IPs instead of 0.0.0.0/0"
echo "🛡️  Consider using SSH tunnel for maximum security"
