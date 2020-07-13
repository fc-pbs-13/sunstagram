from rest_framework.routers import SimpleRouter

from feeds.views import PostViewSet
from users.views import UserViewSet
from profiles.views import UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('profile', UserProfileViewSet)
router.register('posts', PostViewSet)
urlpatterns = router.urls
