"""
Throttling (Rate Limiting) Implementation
Membatasi jumlah request per IP address dalam periode waktu tertentu
"""
from ninja.errors import HttpError
from functools import wraps
from collections import defaultdict
import time


# Request tracker untuk menyimpan history request per IP
request_tracker = defaultdict(list)


def throttle(max_requests: int = 10, time_window: int = 60):
    """
    Decorator untuk rate limiting
    
    Args:
        max_requests: Maksimal jumlah request yang diperbolehkan
        time_window: Periode waktu dalam detik
    
    Usage:
        @throttle(max_requests=10, time_window=60)
        def my_endpoint(request):
            return {"message": "success"}
    
    Raises:
        HttpError 429: Jika request melebihi batas
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Get client IP address
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            current_time = time.time()
            
            # Bersihkan request lama yang sudah melewati time window
            request_tracker[client_ip] = [
                req_time for req_time in request_tracker[client_ip]
                if current_time - req_time < time_window
            ]
            
            # Check apakah sudah mencapai limit
            if len(request_tracker[client_ip]) >= max_requests:
                raise HttpError(
                    429, 
                    f"Rate limit exceeded. Maximum {max_requests} requests per {time_window} seconds."
                )
            
            # Tambahkan request saat ini ke tracker
            request_tracker[client_ip].append(current_time)
            
            # Execute fungsi asli
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def get_request_stats(ip_address: str) -> dict:
    """
    Mendapatkan statistik request untuk IP tertentu
    
    Args:
        ip_address: IP address yang ingin dicek
    
    Returns:
        dict: Informasi tentang jumlah request dalam time window
    """
    current_time = time.time()
    recent_requests = [
        req_time for req_time in request_tracker[ip_address]
        if current_time - req_time < 60
    ]
    
    return {
        "ip_address": ip_address,
        "requests_last_minute": len(recent_requests),
        "total_tracked_requests": len(request_tracker[ip_address])
    }


def clear_old_requests():
    """
    Membersihkan request lama dari tracker (untuk maintenance)
    Dipanggil secara periodik untuk menghemat memori
    """
    current_time = time.time()
    for ip_address in list(request_tracker.keys()):
        request_tracker[ip_address] = [
            req_time for req_time in request_tracker[ip_address]
            if current_time - req_time < 3600  # Keep last 1 hour
        ]
        
        # Hapus IP yang sudah tidak ada request
        if not request_tracker[ip_address]:
            del request_tracker[ip_address]


# Predefined throttle decorators untuk kemudahan penggunaan
def throttle_strict(func):
    """Throttle ketat: 5 requests per 5 menit"""
    return throttle(max_requests=5, time_window=300)(func)


def throttle_moderate(func):
    """Throttle sedang: 20 requests per 1 menit"""
    return throttle(max_requests=20, time_window=60)(func)


def throttle_relaxed(func):
    """Throttle ringan: 100 requests per 1 menit"""
    return throttle(max_requests=100, time_window=60)(func)
