from flask import Blueprint, request, jsonify
from app import db
from app.models import StockQuote
from app.schemas import stock_quote_schema, stock_quotes_schema

stocks_bp = Blueprint('stocks', __name__)

@stocks_bp.route('/', methods=['GET'])
def get_stock_quotes():
    """Get all stock quotes"""
    limit = request.args.get('limit', 10, type=int)
    
    stocks = StockQuote.query.limit(limit).all()
    
    return jsonify({
        'stocks': stock_quotes_schema.dump(stocks),
        'count': len(stocks)
    })

@stocks_bp.route('/<symbol>', methods=['GET'])
def get_stock_by_symbol(symbol):
    """Get a specific stock quote by symbol"""
    stock = StockQuote.query.filter_by(symbol=symbol.upper()).first_or_404()
    return jsonify(stock_quote_schema.dump(stock))

@stocks_bp.route('/trending', methods=['GET'])
def get_trending_stocks():
    """Get trending stocks (highest volume or biggest price changes)"""
    limit = request.args.get('limit', 5, type=int)
    
    # Get stocks with highest volume or biggest price changes
    stocks = StockQuote.query.order_by(StockQuote.volume.desc()).limit(limit).all()
    
    return jsonify({
        'trending_stocks': stock_quotes_schema.dump(stocks),
        'count': len(stocks)
    })

@stocks_bp.route('/', methods=['POST'])
def create_stock_quote():
    """Create a new stock quote"""
    data = request.get_json()
    
    stock = StockQuote(
        symbol=data['symbol'].upper(),
        company_name=data.get('company_name'),
        current_price=data.get('current_price'),
        price_change=data.get('price_change'),
        percent_change=data.get('percent_change'),
        volume=data.get('volume'),
        market_cap=data.get('market_cap')
    )
    
    db.session.add(stock)
    db.session.commit()
    
    return jsonify(stock_quote_schema.dump(stock)), 201

@stocks_bp.route('/<symbol>', methods=['PUT'])
def update_stock_quote(symbol):
    """Update an existing stock quote"""
    stock = StockQuote.query.filter_by(symbol=symbol.upper()).first_or_404()
    data = request.get_json()
    
    stock.company_name = data.get('company_name', stock.company_name)
    stock.current_price = data.get('current_price', stock.current_price)
    stock.price_change = data.get('price_change', stock.price_change)
    stock.percent_change = data.get('percent_change', stock.percent_change)
    stock.volume = data.get('volume', stock.volume)
    stock.market_cap = data.get('market_cap', stock.market_cap)
    
    db.session.commit()
    
    return jsonify(stock_quote_schema.dump(stock))

@stocks_bp.route('/<symbol>', methods=['DELETE'])
def delete_stock_quote(symbol):
    """Delete a stock quote"""
    stock = StockQuote.query.filter_by(symbol=symbol.upper()).first_or_404()
    db.session.delete(stock)
    db.session.commit()
    
    return jsonify({'message': f'Stock quote for {symbol} deleted successfully'}), 200
