from django.shortcuts import render

# Custom 404 error handler
def handler404(request, exception):
    """
    Custom 404 error handler function.
    
    Args:
        request: Django HttpRequest object.
        exception: Exception that triggered the 404 error.

    Returns:
        Rendered 404.html template with a 404 status.
    """
    return render(request, 'user/404.html', status=404)
