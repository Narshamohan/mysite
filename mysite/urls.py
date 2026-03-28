from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.models import User

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

# --- ADDED: Secret Admin Creation Function ---
def setup_admin(request):
    if not User.objects.filter(username='admin').exists():
        # Change 'mypassword123' to whatever you want your secure password to be!
        User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        return HttpResponse("SUCCESS: Admin created! You can now log in.")
    return HttpResponse("Admin already exists. You can log in safely.")
# ---------------------------------------------

urlpatterns = [
    # --- ADDED: Secret URL Route ---
    path("secret-setup-admin/", setup_admin),
    
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]