from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import sys

def health_check(request):
    """Health check endpoint untuk debugging"""
    status = {
        'status': 'ok',
        'debug': settings.DEBUG,
        'python_version': sys.version,
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['database'] = 'connected'
        
        # Check if tables exist
        from courses.models import Course
        course_count = Course.objects.count()
        status['tables_migrated'] = True
        status['course_count'] = course_count
    except Exception as e:
        status['database'] = 'error'
        status['error'] = str(e)
        status['tables_migrated'] = False
    
    return JsonResponse(status)
