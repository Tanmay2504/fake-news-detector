"""
In-memory caching for predictions
"""
import hashlib
import time
from typing import Optional, Dict, Any
from collections import OrderedDict


class PredictionCache:
    """
    LRU cache for storing prediction results
    """
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        Initialize cache
        
        Args:
            max_size: Maximum number of cached items
            ttl: Time to live in seconds (default 1 hour)
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, text: str, mode: str = "ensemble") -> str:
        """
        Generate cache key from text and mode
        
        Args:
            text: Input text
            mode: Prediction mode
            
        Returns:
            Hash key for cache
        """
        content = f"{text}|{mode}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, mode: str = "ensemble") -> Optional[Dict[str, Any]]:
        """
        Get cached prediction if available and not expired
        
        Args:
            text: Input text
            mode: Prediction mode
            
        Returns:
            Cached result or None if not found/expired
        """
        key = self._make_key(text, mode)
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check if expired
            if time.time() - entry['timestamp'] > self.ttl:
                del self.cache[key]
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            return entry['result']
        
        self.misses += 1
        return None
    
    def set(self, text: str, result: Dict[str, Any], mode: str = "ensemble"):
        """
        Store prediction result in cache
        
        Args:
            text: Input text
            result: Prediction result to cache
            mode: Prediction mode
        """
        key = self._make_key(text, mode)
        
        # Remove oldest if at max size
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        self.cache[key] = {
            'result': result,
            'timestamp': time.time()
        }
    
    def clear(self):
        """Clear all cached items"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 3),
            "ttl": self.ttl
        }


# Global cache instance
_cache = None


def get_cache(max_size: int = 1000, ttl: int = 3600) -> PredictionCache:
    """
    Get or create global cache instance (singleton pattern)
    
    Args:
        max_size: Maximum cache size
        ttl: Time to live in seconds
        
    Returns:
        PredictionCache instance
    """
    global _cache
    if _cache is None:
        _cache = PredictionCache(max_size=max_size, ttl=ttl)
    return _cache
