from rest_framework.routers import SimpleRouter
from accounts.views import AccountViewSet
from accounts_profile.views import AccountProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('users', AccountViewSet, basename='users')
router.register('profile', AccountProfileViewSet, basename='profile')
urlpatterns = router.urls
