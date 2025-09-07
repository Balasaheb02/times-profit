from flask import Blueprint, jsonify, render_template_string, request
from app import db
from sqlalchemy import text
import os

# Create blueprint
db_admin_bp = Blueprint('db_admin', __name__)

# Simple HTML template for database viewer
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Times Profit Database Admin</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { 
            background: rgba(255,255,255,0.95); 
            backdrop-filter: blur(10px);
            border-radius: 15px; 
            padding: 30px; 
            margin-bottom: 30px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .nav { 
            background: rgba(255,255,255,0.95); 
            backdrop-filter: blur(10px);
            padding: 20px; 
            border-radius: 15px; 
            margin-bottom: 30px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }
        .nav a { 
            padding: 12px 20px; 
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; 
            text-decoration: none; 
            border-radius: 25px; 
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
        }
        .nav a:hover { 
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102,126,234,0.4);
        }
        .content { 
            background: rgba(255,255,255,0.95); 
            backdrop-filter: blur(10px);
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        table { 
            border-collapse: collapse; 
            width: 100%; 
            margin: 20px 0; 
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        th, td { 
            padding: 15px; 
            text-align: left; 
            border-bottom: 1px solid #eee;
        }
        th { 
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; 
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }
        tr:nth-child(even) { background-color: #f8f9fa; }
        tr:hover { background-color: #e3f2fd; transition: all 0.3s ease; }
        .info, .error, .success { 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .info { 
            background: linear-gradient(45deg, #e3f2fd, #f3e5f5); 
            border-left: 5px solid #2196f3; 
            color: #1565c0;
        }
        .error { 
            background: linear-gradient(45deg, #ffebee, #fce4ec); 
            border-left: 5px solid #f44336; 
            color: #c62828;
        }
        .success { 
            background: linear-gradient(45deg, #e8f5e8, #f1f8e9); 
            border-left: 5px solid #4caf50; 
            color: #2e7d32;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: linear-gradient(45deg, #f8f9fa, #e9ecef);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        .pagination a, .pagination span {
            padding: 10px 15px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        .pagination a:hover {
            background: #764ba2;
            transform: translateY(-2px);
        }
        .pagination .current {
            background: #764ba2;
        }
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .nav { flex-direction: column; }
            .nav a { justify-content: center; }
            table { font-size: 0.9em; }
            th, td { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗄️ Times Profit Database Administration</h1>
            <p style="margin-top: 10px; color: #666; font-size: 1.1em;">
                Comprehensive database viewer and management interface
            </p>
        </div>
        
        <div class="nav">
            <a href="/api/admin/db">📊 Dashboard</a>
            <a href="/api/admin/db/tables">📋 All Tables</a>
            <a href="/api/admin/db/table/articles">📰 Articles</a>
            <a href="/api/admin/db/table/categories">🏷️ Categories</a>
            <a href="/api/admin/db/table/authors">👤 Authors</a>
            <a href="/api/admin/db/stats">📈 Statistics</a>
        </div>
        
        <div class="content">
            {{ content | safe }}
        </div>
    </div>
</body>
</html>
'''

def get_db_connection():
    """Get database connection from Flask-SQLAlchemy"""
    return db.session

@db_admin_bp.route('/api/admin/db')
def dashboard():
    """Database dashboard"""
    try:
        # Get database info
        result = db.session.execute(text("SELECT current_database(), current_user, version()"))
        db_info = result.fetchone()
        
        # Get table count
        result = db.session.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"))
        table_count = result.fetchone()[0]
        
        # Get total records in main tables
        stats = {}
        main_tables = ['articles', 'categories', 'authors', 'users', 'tags']
        
        for table in main_tables:
            try:
                result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                stats[table] = result.fetchone()[0]
            except:
                stats[table] = "N/A"
        
        content = f"""
        <div class="success">
            <h2>✅ Database Connection Successful</h2>
            <div style="margin-top: 15px;">
                <p><strong>Database:</strong> {db_info[0]}</p>
                <p><strong>User:</strong> {db_info[1]}</p>
                <p><strong>Total Tables:</strong> {table_count}</p>
            </div>
        </div>
        
        <h2 style="margin: 30px 0 20px 0;">📊 Quick Statistics</h2>
        <div class="stats-grid">
        """
        
        for table, count in stats.items():
            icon = {"articles": "📰", "categories": "🏷️", "authors": "👤", "users": "👥", "tags": "🏷️"}.get(table, "📋")
            content += f"""
            <div class="stat-card">
                <div style="font-size: 2em; margin-bottom: 10px;">{icon}</div>
                <div class="stat-number">{count}</div>
                <div style="text-transform: capitalize; margin-top: 5px;">{table}</div>
            </div>
            """
        
        content += """
        </div>
        
        <h2 style="margin: 30px 0 20px 0;">🔧 Quick Actions</h2>
        <div class="nav">
            <a href="/api/admin/db/tables">🔍 Browse All Tables</a>
            <a href="/api/admin/db/table/articles">📰 View Articles</a>
            <a href="/api/admin/db/stats">📊 Detailed Statistics</a>
            <a href="/api/admin/tables-json">🔗 JSON API - Tables</a>
        </div>
        """
        
        return render_template_string(HTML_TEMPLATE, content=content)
        
    except Exception as e:
        content = f'<div class="error">❌ Database Error: {str(e)}</div>'
        return render_template_string(HTML_TEMPLATE, content=content)

@db_admin_bp.route('/api/admin/db/tables')
def list_tables():
    """List all database tables"""
    try:
        result = db.session.execute(text("""
            SELECT 
                tablename, 
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """))
        
        tables = result.fetchall()
        
        content = "<h2>📋 Database Tables</h2>"
        content += "<table><tr><th>Table Name</th><th>Size</th><th>Actions</th></tr>"
        
        for table, size in tables:
            content += f"""
            <tr>
                <td><strong>{table}</strong></td>
                <td>{size}</td>
                <td>
                    <a href="/api/admin/db/table/{table}" style="margin-right: 10px; color: #667eea;">📊 View Data</a>
                    <a href="/api/admin/db/structure/{table}" style="color: #764ba2;">🏗️ Structure</a>
                </td>
            </tr>
            """
        
        content += "</table>"
        
        return render_template_string(HTML_TEMPLATE, content=content)
        
    except Exception as e:
        content = f'<div class="error">❌ Error: {str(e)}</div>'
        return render_template_string(HTML_TEMPLATE, content=content)

@db_admin_bp.route('/api/admin/db/table/<table_name>')
def view_table(table_name):
    """View table data"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page
        
        # Get column info
        result = db.session.execute(text(f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' AND table_schema = 'public'
            ORDER BY ordinal_position
        """))
        columns_info = result.fetchall()
        columns = [col[0] for col in columns_info]
        
        # Get total count
        result = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        total_count = result.fetchone()[0]
        
        # Get data with proper ordering
        order_clause = "ORDER BY id DESC" if "id" in columns else "ORDER BY 1"
        result = db.session.execute(text(f"SELECT * FROM {table_name} {order_clause} LIMIT {per_page} OFFSET {offset}"))
        rows = result.fetchall()
        
        # Build content
        content = f"""
        <div class="info">
            <h2>📋 Table: {table_name}</h2>
            <p>Total records: <strong>{total_count:,}</strong> | Showing page {page} ({len(rows)} records)</p>
        </div>
        """
        
        # Pagination
        total_pages = (total_count + per_page - 1) // per_page
        if total_pages > 1:
            content += '<div class="pagination">'
            if page > 1:
                content += f'<a href="/api/admin/db/table/{table_name}?page={page-1}">← Previous</a>'
            
            # Show page numbers around current page
            start_page = max(1, page - 2)
            end_page = min(total_pages, page + 2)
            
            for p in range(start_page, end_page + 1):
                if p == page:
                    content += f'<span class="current">{p}</span>'
                else:
                    content += f'<a href="/api/admin/db/table/{table_name}?page={p}">{p}</a>'
            
            if page < total_pages:
                content += f'<a href="/api/admin/db/table/{table_name}?page={page+1}">Next →</a>'
            content += '</div>'
        
        # Data table
        if rows:
            content += "<table><tr>"
            for col in columns:
                content += f"<th>{col}</th>"
            content += "</tr>"
            
            for row in rows:
                content += "<tr>"
                for i, cell in enumerate(row):
                    # Handle different data types
                    if cell is None:
                        cell_str = '<em style="color: #999;">NULL</em>'
                    elif isinstance(cell, bool):
                        cell_str = '✅' if cell else '❌'
                    else:
                        cell_str = str(cell)
                        # Truncate long text
                        if len(cell_str) > 100:
                            cell_str = cell_str[:100] + '...'
                    content += f"<td>{cell_str}</td>"
                content += "</tr>"
            
            content += "</table>"
        else:
            content += '<div class="info">No data found in this table.</div>'
        
        return render_template_string(HTML_TEMPLATE, content=content)
        
    except Exception as e:
        content = f'<div class="error">❌ Error viewing table {table_name}: {str(e)}</div>'
        return render_template_string(HTML_TEMPLATE, content=content)

@db_admin_bp.route('/api/admin/db/structure/<table_name>')
def table_structure(table_name):
    """View table structure"""
    try:
        # Get column details
        result = db.session.execute(text(f"""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default,
                ordinal_position
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' AND table_schema = 'public'
            ORDER BY ordinal_position
        """))
        
        columns = result.fetchall()
        
        content = f"""
        <h2>🏗️ Table Structure: {table_name}</h2>
        <table>
            <tr>
                <th>Position</th>
                <th>Column Name</th>
                <th>Data Type</th>
                <th>Max Length</th>
                <th>Nullable</th>
                <th>Default</th>
            </tr>
        """
        
        for col in columns:
            nullable = "✅" if col[3] == "YES" else "❌"
            max_length = col[2] if col[2] else "N/A"
            default = col[4] if col[4] else "None"
            
            content += f"""
            <tr>
                <td>{col[5]}</td>
                <td><strong>{col[0]}</strong></td>
                <td>{col[1]}</td>
                <td>{max_length}</td>
                <td>{nullable}</td>
                <td>{default}</td>
            </tr>
            """
        
        content += "</table>"
        
        # Get indexes
        try:
            result = db.session.execute(text(f"""
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE tablename = '{table_name}' AND schemaname = 'public'
            """))
            indexes = result.fetchall()
            
            if indexes:
                content += "<h3 style='margin-top: 30px;'>📇 Indexes</h3><table>"
                content += "<tr><th>Index Name</th><th>Definition</th></tr>"
                for idx in indexes:
                    content += f"<tr><td><strong>{idx[0]}</strong></td><td>{idx[1]}</td></tr>"
                content += "</table>"
        except:
            pass
        
        return render_template_string(HTML_TEMPLATE, content=content)
        
    except Exception as e:
        content = f'<div class="error">❌ Error viewing structure for {table_name}: {str(e)}</div>'
        return render_template_string(HTML_TEMPLATE, content=content)

@db_admin_bp.route('/api/admin/db/stats')
def database_stats():
    """Database statistics"""
    try:
        # Database size
        result = db.session.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))"))
        db_size = result.fetchone()[0]
        
        # Table statistics
        result = db.session.execute(text("""
            SELECT 
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_rows,
                n_dead_tup as dead_rows
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC
        """))
        
        table_stats = result.fetchall()
        
        content = f"""
        <h2>📈 Database Statistics</h2>
        <div class="info">
            <h3>💾 Database Size: {db_size}</h3>
        </div>
        
        <h3 style="margin: 30px 0 20px 0;">📊 Table Statistics</h3>
        <table>
            <tr>
                <th>Table</th>
                <th>Live Rows</th>
                <th>Dead Rows</th>
                <th>Inserts</th>
                <th>Updates</th>
                <th>Deletes</th>
            </tr>
        """
        
        for stats in table_stats:
            content += f"""
            <tr>
                <td>
                    <a href="/api/admin/db/table/{stats[0]}" style="color: #667eea; text-decoration: none;">
                        <strong>{stats[0]}</strong>
                    </a>
                </td>
                <td>{stats[4]:,}</td>
                <td>{stats[5]:,}</td>
                <td>{stats[1]:,}</td>
                <td>{stats[2]:,}</td>
                <td>{stats[3]:,}</td>
            </tr>
            """
        
        content += "</table>"
        
        return render_template_string(HTML_TEMPLATE, content=content)
        
    except Exception as e:
        content = f'<div class="error">❌ Error: {str(e)}</div>'
        return render_template_string(HTML_TEMPLATE, content=content)

# JSON API endpoints for your frontend
@db_admin_bp.route('/api/admin/tables-json')
def tables_json():
    """JSON API for tables list"""
    try:
        result = db.session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"))
        tables = [row[0] for row in result.fetchall()]
        
        return jsonify({"tables": tables, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@db_admin_bp.route('/api/admin/table-json/<table_name>')
def table_data_json(table_name):
    """JSON API for table data"""
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get columns
        result = db.session.execute(text(f"""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = '{table_name}' AND table_schema = 'public'
            ORDER BY ordinal_position
        """))
        columns = [row[0] for row in result.fetchall()]
        
        # Get data
        order_clause = "ORDER BY id DESC" if "id" in columns else "ORDER BY 1"
        result = db.session.execute(text(f"SELECT * FROM {table_name} {order_clause} LIMIT {limit} OFFSET {offset}"))
        rows = result.fetchall()
        
        # Get total count
        result = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        total = result.fetchone()[0]
        
        data = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                if i < len(columns):
                    row_dict[columns[i]] = value
            data.append(row_dict)
        
        return jsonify({
            "table": table_name,
            "columns": columns,
            "data": data,
            "total": total,
            "limit": limit,
            "offset": offset,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@db_admin_bp.route('/api/admin/stats-json')
def stats_json():
    """JSON API for database statistics"""
    try:
        # Get table counts
        main_tables = ['articles', 'categories', 'authors', 'users', 'tags']
        stats = {}
        
        for table in main_tables:
            try:
                result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                stats[table] = result.fetchone()[0]
            except:
                stats[table] = 0
        
        # Get database size
        try:
            result = db.session.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))"))
            db_size = result.fetchone()[0]
        except:
            db_size = "Unknown"
        
        return jsonify({
            "table_counts": stats,
            "database_size": db_size,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
