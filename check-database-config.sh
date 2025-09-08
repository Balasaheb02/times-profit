#!/bin/bash

echo "🔍 Database Connection Prerequisites Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Run these commands on your VPS to gather connection information:"
echo ""

echo "1. 📊 Check PostgreSQL status:"
echo "   sudo systemctl status postgresql"
echo ""

echo "2. 🔍 Find database credentials:"
echo "   cat /home/newsapp/times-profit/backend/.env"
echo ""

echo "3. 📋 List databases:"
echo "   sudo -u postgres psql -l"
echo ""

echo "4. 🌐 Check PostgreSQL configuration:"
echo "   sudo cat /etc/postgresql/*/main/postgresql.conf | grep listen_addresses"
echo "   sudo cat /etc/postgresql/*/main/pg_hba.conf | grep -v '^#' | grep -v '^$'"
echo ""

echo "5. 🔧 Check firewall status:"
echo "   sudo ufw status"
echo ""

echo "6. 📡 Test local connection:"
echo "   psql -h localhost -U newsuser -d newsdb"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Copy the output of these commands and we'll configure DBeaver accordingly!"
