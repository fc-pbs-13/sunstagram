from rest_framework.routers import SimpleRouter
from users.views import UserViewSet
from profiles.views import UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('profile', UserProfileViewSet)
urlpatterns = router.urls
