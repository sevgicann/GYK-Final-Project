# Terramind Database Architecture

## Overview
This document describes the database architecture for the Terramind agricultural recommendation system. The database is designed with a clear separation between master tables and transaction tables, optimized for performance and scalability.

## Database Design Principles

### Master Tables
Master tables store core business entities that are referenced by transaction tables:
- **users**: User accounts and profiles
- **products**: Agricultural products and their requirements
- **environments**: User-defined environmental locations

### Transaction Tables
Transaction tables store business operations and model results:
- **recommendations**: AI-generated recommendations (transaction)
- **model_results**: ML model predictions and results (transaction)
- **user_activity_logs**: User activity tracking (transaction)

## Table Structure

### Master Tables

#### users
```sql
- id (UUID, Primary Key)
- name (String, Required)
- email (String, Unique, Required)
- password_hash (String, Required) - Werkzeug hashed
- language (String, Default: 'tr')
- is_active (Boolean, Default: true)
- last_login (DateTime)
- created_at (DateTime)
- updated_at (DateTime)
- city (String)
- district (String)
- latitude (Float)
- longitude (Float)
- is_gps_enabled (Boolean)
- notifications_enabled (Boolean)
- theme (String)
```

#### products
```sql
- id (UUID, Primary Key)
- name (String, Required, Indexed)
- category (String, Required, Indexed)
- description (Text)
- image_url (String)
- is_active (Boolean, Default: true)
- created_at (DateTime)
- updated_at (DateTime)
```

#### product_requirements
```sql
- id (UUID, Primary Key)
- product_id (UUID, Foreign Key to products)
- ph_min/max (Float)
- nitrogen_min/max (Float)
- phosphorus_min/max (Float)
- potassium_min/max (Float)
- humidity_min/max (Float)
- temperature_min/max (Float)
- rainfall_min/max (Float)
- notes (Text)
- created_at (DateTime)
- updated_at (DateTime)
```

#### environments
```sql
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to users)
- name (String, Required)
- location_type (String, Default: 'manual')
- is_active (Boolean, Default: true)
- city (String)
- district (String)
- latitude (Float)
- longitude (Float)
- created_at (DateTime)
- updated_at (DateTime)
```

#### environment_data
```sql
- id (UUID, Primary Key)
- environment_id (UUID, Foreign Key to environments)
- ph (Float)
- nitrogen (Float)
- phosphorus (Float)
- potassium (Float)
- organic_matter (Float)
- soil_type (String)
- temperature (Float)
- humidity (Float)
- rainfall (Float)
- sunlight_hours (Float)
- wind_speed (Float)
- altitude (Float)
- slope (Float)
- drainage (String)
- data_source (String, Default: 'manual')
- measured_at (DateTime)
- created_at (DateTime)
```

### Transaction Tables

#### recommendations
```sql
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to users)
- product_id (UUID, Foreign Key to products)
- environment_id (UUID, Foreign Key to environments)
- model_result_id (UUID, Foreign Key to model_results)
- recommendation_type (String, Required)
- confidence_score (Float, 0.0-1.0)
- suitability_score (Float, 0.0-1.0)
- model_type (String, Required)
- model_version (String, Required)
- algorithm (String, Required)
- title (String, Required)
- description (Text, Required)
- benefits (Text)
- challenges (Text)
- suggestions (Text)
- input_parameters (JSON)
- status (String, Default: 'active')
- is_favorite (Boolean, Default: false)
- view_count (Integer, Default: 0)
- last_viewed_at (DateTime)
- created_at (DateTime)
- updated_at (DateTime)
```

#### model_results
```sql
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to users)
- model_type (String, Required)
- model_version (String, Required)
- algorithm (String, Required)
- input_data (JSON, Required)
- predictions (JSON, Required)
- confidence_scores (JSON)
- processing_time_ms (Float)
- top_recommendations (JSON)
- recommendation_type (String)
- status (String, Default: 'completed')
- error_message (Text)
- created_at (DateTime)
- completed_at (DateTime)
```

#### user_activity_logs
```sql
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to users)
- activity_type (String, Required)
- activity_category (String, Required)
- description (String, Required)
- details (JSON)
- request_method (String)
- endpoint (String)
- ip_address (String)
- user_agent (Text)
- status (String, Default: 'success')
- status_code (Integer)
- error_message (Text)
- response_time_ms (Float)
- memory_usage_mb (Float)
- session_id (String)
- device_type (String)
- platform (String)
- created_at (DateTime)
```

## Database Optimizations

### PostgreSQL Configuration
- **Encoding**: UTF-8 with Turkish locale support
- **Extensions**: UUID, pg_stat_statements, unaccent, btree_gin, btree_gist
- **Performance tuning**: Optimized for 200 max connections, 256MB shared buffers
- **Monitoring**: pg_stat_statements enabled for query analysis

### Redis Configuration
- **Memory limit**: 256MB with LRU eviction
- **Persistence**: RDB + AOF for data durability
- **Performance**: Optimized for caching and session storage

### Indexing Strategy
- **Primary indexes**: All UUID primary keys
- **Foreign key indexes**: All foreign key relationships
- **Composite indexes**: Common query patterns (user_id + status, etc.)
- **JSON indexes**: GIN indexes on JSON fields for fast searches
- **Text search indexes**: Trigram indexes for product name/description search
- **Partial indexes**: Active records only where applicable

## Security Features

### Authentication
- **Password hashing**: Werkzeug's secure password hashing
- **JWT tokens**: 7-day access tokens, 30-day refresh tokens
- **Session management**: Redis-based session storage

### Data Protection
- **Input validation**: All user inputs validated and sanitized
- **SQL injection prevention**: SQLAlchemy ORM with parameterized queries
- **XSS protection**: Output encoding and validation
- **CSRF protection**: Flask-WTF CSRF tokens

## Performance Monitoring

### Query Performance
- **pg_stat_statements**: Track slow queries and optimization opportunities
- **Connection pooling**: Efficient database connection management
- **Query caching**: Redis-based query result caching

### Application Monitoring
- **Activity logging**: Comprehensive user activity tracking
- **Performance metrics**: Response time and memory usage tracking
- **Error tracking**: Detailed error logging and monitoring

## Migration Strategy

### Database Migrations
- **Flask-Migrate**: Automated schema migrations
- **Version control**: All schema changes tracked in Git
- **Rollback support**: Safe migration rollback procedures

### Data Migration
- **Backup strategy**: Regular automated backups
- **Data validation**: Post-migration data integrity checks
- **Performance testing**: Load testing after major changes

## Usage Examples

### Creating a User
```python
user = User(
    name="John Doe",
    email="john@example.com",
    language="tr",
    city="Ankara",
    district="Çankaya"
)
user.set_password("securepassword")
db.session.add(user)
db.session.commit()
```

### Logging Activity
```python
UserActivityLog.log_activity(
    user_id=user.id,
    activity_type="recommendation_request",
    activity_category="recommendation",
    description="User requested crop recommendation",
    ip_address=request.remote_addr,
    device_type="mobile",
    platform="flutter"
)
```

### Creating Model Result
```python
model_result = ModelResult.create_result(
    user_id=user.id,
    model_type="crop_recommendation",
    model_version="v1.0",
    algorithm="lightgbm",
    input_data=input_data,
    predictions=predictions,
    confidence_scores=confidence_scores,
    processing_time_ms=150.5
)
```

## Maintenance

### Regular Tasks
- **Log cleanup**: Remove old activity logs (90+ days)
- **Index maintenance**: Rebuild indexes for optimal performance
- **Statistics update**: Update table statistics for query planner
- **Backup verification**: Test backup restoration procedures

### Monitoring Alerts
- **Connection limits**: Alert when approaching max connections
- **Disk space**: Monitor database disk usage
- **Query performance**: Alert on slow queries (>1 second)
- **Error rates**: Monitor application error rates

## Future Enhancements

### Planned Features
- **Read replicas**: Separate read/write database instances
- **Partitioning**: Partition large tables by date/user
- **Full-text search**: Advanced search capabilities
- **Real-time analytics**: Live dashboard with database metrics
- **Automated scaling**: Auto-scale based on load metrics
