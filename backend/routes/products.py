from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# Product will be imported from app
# User will be imported from app
from flask import current_app

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        # Query parameters
        category = request.args.get('category')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        from app import Product
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(
                current_app.extensions['sqlalchemy'].db.or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        # Pagination
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'products': [product.to_dict() for product in products.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': products.total,
                    'pages': products.pages,
                    'has_next': products.has_next,
                    'has_prev': products.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch products',
            'error': str(e)
        }), 500

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        from app import Product
        product = Product.query.get(product_id)
        
        if not product or not product.is_active:
            return jsonify({
                'success': False,
                'message': 'Product not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'product': product.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch product',
            'error': str(e)
        }), 500

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        from app import Product
        categories = Product.get_all_categories()
        
        return jsonify({
            'success': True,
            'data': {
                'categories': categories
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch categories',
            'error': str(e)
        }), 500

@products_bp.route('/search', methods=['GET'])
def search_products():
    """Search products by name or description"""
    try:
        query = (request.args.get('q') or '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Search query is required'
            }), 400
        
        from app import Product
        products = Product.search_products(query)
        
        return jsonify({
            'success': True,
            'data': {
                'products': [product.to_dict() for product in products],
                'query': query,
                'count': len(products)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Search failed',
            'error': str(e)
        }), 500

@products_bp.route('/recommend', methods=['POST'])
@jwt_required()
def recommend_products():
    """Recommend products based on environment data"""
    try:
        user_id = get_jwt_identity()
        from app import User
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Environment data is required'
            }), 400
        
        # Get environment data from request
        ph = data.get('ph')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        rainfall = data.get('rainfall')
        
        # Get all products
        from app import Product
        products = Product.query.filter_by(is_active=True).all()
        recommendations = []
        
        for product in products:
            if product.requirements:
                # Check suitability
                suitable, issues = product.requirements.is_suitable_for_environment(data)
                
                # Calculate suitability score
                score = 0.0
                if suitable:
                    score = 1.0
                else:
                    # Calculate partial score based on how many requirements are met
                    total_checks = 0
                    passed_checks = 0
                    
                    if product.requirements.ph_min is not None or product.requirements.ph_max is not None:
                        total_checks += 1
                        if ph and product.requirements.ph_min <= ph <= product.requirements.ph_max:
                            passed_checks += 1
                    
                    if product.requirements.temperature_min is not None or product.requirements.temperature_max is not None:
                        total_checks += 1
                        if temperature and product.requirements.temperature_min <= temperature <= product.requirements.temperature_max:
                            passed_checks += 1
                    
                    if product.requirements.humidity_min is not None or product.requirements.humidity_max is not None:
                        total_checks += 1
                        if humidity and product.requirements.humidity_min <= humidity <= product.requirements.humidity_max:
                            passed_checks += 1
                    
                    if total_checks > 0:
                        score = passed_checks / total_checks
                
                recommendations.append({
                    'product': product.to_dict(),
                    'suitability_score': score,
                    'suitable': suitable,
                    'issues': issues
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'environment_data': data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to generate recommendations',
            'error': str(e)
        }), 500

@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    """Create a new product (Admin only)"""
    try:
        user_id = get_jwt_identity()
        from app import User
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # TODO: Add admin check here
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Product data is required'
            }), 400
        
        # Validate required fields
        name = (data.get('name') or '').strip()
        category = (data.get('category') or '').strip()
        description = (data.get('description') or '').strip()
        
        if not name:
            return jsonify({
                'success': False,
                'message': 'Product name is required'
            }), 400
        
        if not category:
            return jsonify({
                'success': False,
                'message': 'Product category is required'
            }), 400
        
        # Create product
        product = Product(
            name=name,
            category=category,
            description=description,
            image_url=data.get('image_url')
        )
        
        current_app.extensions['sqlalchemy'].db.session.add(product)
        current_app.extensions['sqlalchemy'].db.session.flush()  # Get the product ID
        
        # Create requirements if provided
        requirements_data = data.get('requirements')
        if requirements_data:
            requirements = ProductRequirements(
                product_id=product.id,
                ph_min=requirements_data.get('ph', {}).get('min'),
                ph_max=requirements_data.get('ph', {}).get('max'),
                nitrogen_min=requirements_data.get('nitrogen', {}).get('min'),
                nitrogen_max=requirements_data.get('nitrogen', {}).get('max'),
                phosphorus_min=requirements_data.get('phosphorus', {}).get('min'),
                phosphorus_max=requirements_data.get('phosphorus', {}).get('max'),
                potassium_min=requirements_data.get('potassium', {}).get('min'),
                potassium_max=requirements_data.get('potassium', {}).get('max'),
                humidity_min=requirements_data.get('humidity', {}).get('min'),
                humidity_max=requirements_data.get('humidity', {}).get('max'),
                temperature_min=requirements_data.get('temperature', {}).get('min'),
                temperature_max=requirements_data.get('temperature', {}).get('max'),
                rainfall_min=requirements_data.get('rainfall', {}).get('min'),
                rainfall_max=requirements_data.get('rainfall', {}).get('max'),
                notes=requirements_data.get('notes')
            )
            
            current_app.extensions['sqlalchemy'].db.session.add(requirements)
        
        current_app.extensions['sqlalchemy'].db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'data': {
                'product': product.to_dict()
            }
        }), 201
        
    except Exception as e:
        current_app.extensions['sqlalchemy'].db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to create product',
            'error': str(e)
        }), 500
