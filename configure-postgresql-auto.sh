#!/bin/bash

echo "🔧 Configuring PostgreSQL for DBeaver Remote Access"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Run these commands on your VPS to enable remote access:"
echo ""

# Step 1: Configure PostgreSQL to listen on all addresses
echo "1. 📝 Edit PostgreSQL configuration:"
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf

echo "✅ Updated listen_addresses to '*'"

# Step 2: Add remote access rule to pg_hba.conf
echo ""
echo "2. 🔐 Add remote access rule:"
echo "host    all             all             0.0.0.0/0               md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf > /dev/null

echo "✅ Added remote access rule"

# Step 3: Restart PostgreSQL
echo ""
echo "3. 🔄 Restarting PostgreSQL:"
sudo systemctl restart postgresql

echo "✅ PostgreSQL restarted"

# Step 4: Enable firewall rule
echo ""
echo "4. 🔥 Opening firewall port 5432:"
sudo ufw allow 5432

echo "✅ Port 5432 opened"

# Step 5: Verify configuration
echo ""
echo "5. ✅ Verifying configuration:"
echo ""

echo "📊 PostgreSQL status:"
sudo systemctl status postgresql --no-pager -l

echo ""
echo "🌐 Listening addresses:"
sudo netstat -tlnp | grep 5432

echo ""
echo "🔒 Authentication config:"
sudo tail -n 5 /etc/postgresql/*/main/pg_hba.conf

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PostgreSQL is now configured for remote access!"
echo ""
echo "🔗 DBeaver Connection Details:"
echo "   Host: $(curl -s ifconfig.me)"
echo "   Port: 5432"
echo "   Database: newsdb"
echo "   Username: newsuser"
echo "   Password: YourSecurePassword123!"
echo ""
echo "🧪 Test connection:"
echo "   psql -h $(curl -s ifconfig.me) -U newsuser -d newsdb"
