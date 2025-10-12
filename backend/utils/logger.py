"""
Logging configuration and utilities for Terramind Backend API
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from functools import wraps
import time
from typing import Any, Callable, Dict, Optional

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        # Add timestamp
        record.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return super().format(record)

class TerramindLogger:
    """Centralized logging configuration for Terramind API"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logging()
            TerramindLogger._initialized = True
    
    def _setup_logging(self):
        """Setup logging configuration"""
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Get log level from environment
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Create main logger
        self.logger = logging.getLogger('terramind')
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level, logging.INFO))
        
        console_formatter = ColoredFormatter(
            '%(timestamp)s | %(levelname)-8s | %(name)-20s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler for all logs
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'terramind.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-15s:%(lineno)-4d | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'errors.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
        
        # Log startup message
        self.logger.info("[STARTUP] Terramind Logger initialized successfully")
        self.logger.info(f"[CONFIG] Log directory: {log_dir}")
        self.logger.info(f"[CONFIG] Log level: {log_level}")
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """Get a logger instance with the specified name"""
        if name:
            return logging.getLogger(f'terramind.{name}')
        return self.logger

# Global logger instance
terramind_logger = TerramindLogger()

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance"""
    return terramind_logger.get_logger(name)

def log_function_call(func: Callable) -> Callable:
    """Decorator to log function calls with parameters and execution time"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Get function info
        func_name = f"{func.__module__}.{func.__name__}"
        start_time = time.time()
        
        # Log function entry
        logger.info(f"[ENTER] {func_name}")
        
        # Log parameters (excluding sensitive data)
        if args:
            safe_args = []
            for arg in args:
                if isinstance(arg, (str, int, float, bool, type(None))):
                    safe_args.append(str(arg))
                else:
                    safe_args.append(f"<{type(arg).__name__}>")
            logger.debug(f"[ARGS] {safe_args}")
        
        if kwargs:
            safe_kwargs = {}
            sensitive_keys = {'password', 'token', 'secret', 'key', 'auth'}
            for key, value in kwargs.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    safe_kwargs[key] = "***"
                elif isinstance(value, (str, int, float, bool, type(None))):
                    safe_kwargs[key] = str(value)
                else:
                    safe_kwargs[key] = f"<{type(value).__name__}>"
            logger.debug(f"[KWARGS] {safe_kwargs}")
        
        try:
            # Execute function
            result = func(*args, **kwargs)
            
            # Log function exit
            execution_time = time.time() - start_time
            logger.info(f"[EXIT] {func_name} (took {execution_time:.3f}s)")
            
            # Log result type (not the actual result for performance)
            if result is not None:
                logger.debug(f"[RESULT] <{type(result).__name__}>")
            
            return result
            
        except Exception as e:
            # Log function error
            execution_time = time.time() - start_time
            logger.error(f"[ERROR] {func_name} failed after {execution_time:.3f}s - {str(e)}")
            logger.exception(f"[EXCEPTION] Details for {func_name}")
            raise
    
    return wrapper

def log_api_call(func: Callable) -> Callable:
    """Decorator specifically for API endpoint logging"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger('api')
        
        # Try to get request info from Flask context
        try:
            from flask import request
            method = request.method
            endpoint = request.endpoint
            remote_addr = request.remote_addr
            user_agent = request.headers.get('User-Agent', 'Unknown')
            
            logger.info(f"[API] {method} {endpoint} from {remote_addr}")
            logger.debug(f"[USER-AGENT] {user_agent}")
            
        except Exception:
            # If not in Flask context, use function name
            logger.info(f"[API] {func.__name__}")
        
        return log_function_call(func)(*args, **kwargs)
    
    return wrapper

def log_database_operation(func: Callable) -> Callable:
    """Decorator for database operations"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger('database')
        
        operation = func.__name__
        logger.info(f"[DB] {operation}")
        
        return log_function_call(func)(*args, **kwargs)
    
    return wrapper

def log_business_logic(func: Callable) -> Callable:
    """Decorator for business logic functions"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger('business')
        
        logic_name = func.__name__
        logger.info(f"[BUSINESS] {logic_name}")
        
        return log_function_call(func)(*args, **kwargs)
    
    return wrapper

# Convenience functions for different log levels
def log_info(message: str, logger_name: str = None):
    """Log info message"""
    get_logger(logger_name).info(f"[INFO] {message}")

def log_warning(message: str, logger_name: str = None):
    """Log warning message"""
    get_logger(logger_name).warning(f"[WARNING] {message}")

def log_error(message: str, logger_name: str = None):
    """Log error message"""
    get_logger(logger_name).error(f"[ERROR] {message}")

def log_debug(message: str, logger_name: str = None):
    """Log debug message"""
    get_logger(logger_name).debug(f"[DEBUG] {message}")

def log_success(message: str, logger_name: str = None):
    """Log success message"""
    get_logger(logger_name).info(f"[SUCCESS] {message}")

def log_performance(operation: str, duration: float, logger_name: str = None):
    """Log performance metrics"""
    get_logger(logger_name).info(f"[PERFORMANCE] {operation} took {duration:.3f}s")

# Initialize logger on import
if __name__ != "__main__":
    # This ensures logger is initialized when module is imported
    pass
