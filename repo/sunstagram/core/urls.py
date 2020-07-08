from rest_framework.routers import SimpleRouter

from feeds.views import PhotoViewSet
from users.views import UserViewSet
from profiles.views import UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('profile', UserProfileViewSet)
router.register('photos', PhotoViewSet)
urlpatterns = router.urls
