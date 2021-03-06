from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from comments.views import CommentViewSet
from feeds.views import PostViewSet, TagPostViewSet, SearchTagViewSet
from follows.views import FollowViewSet, ParentViewSet
from likes.views import PostLikeViewSet, CommentLikeViewSet, ReplyLikeViewSet
from photos.views import PhotoViewSet
from replies.views import ReplyViewSet
from stories.views import StoryViewSet
from users.views import UserViewSet
from profiles.views import UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'profile', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'replies', ReplyViewSet)
router.register(r'post_likes', PostLikeViewSet)
router.register(r'comment_likes', CommentLikeViewSet)
router.register(r'reply_likes', ReplyLikeViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'stories', StoryViewSet)
router.register(r'tags', SearchTagViewSet)
router.register(r'parents', ParentViewSet)


"""
users/123/posts/456
users/123/photos/456
users/123/profile/456
users/123/follows/456
users/123/stories/456
users/123/following
users/123/followers
users/123/stories
"""
users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
users_router.register(r'posts', PostViewSet)
users_router.register(r'photos', PhotoViewSet)
users_router.register(r'profile', UserProfileViewSet)
users_router.register(r'follows', FollowViewSet)
users_router.register(r'stories', StoryViewSet)

"""
users/123/posts/456/photos/789
"""
users_posts_router = routers.NestedSimpleRouter(users_router, r'posts')
users_posts_router.register(r'photos', PhotoViewSet)

"""
posts/123/photos/456
posts/123/comments/456
posts/123/post_likes/456
posts/123/tags/456
"""
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'photos', PhotoViewSet)
posts_router.register(r'comments', CommentViewSet)
posts_router.register(r'post_likes', PostLikeViewSet)
posts_router.register(r'tags', TagPostViewSet)

"""
comments/123/replies/456
comments/123/comment_likes/456
"""
comments_router = routers.NestedSimpleRouter(router, r'comments', lookup='comment')
comments_router.register(r'replies', ReplyViewSet)
comments_router.register(r'comment_likes', CommentLikeViewSet)

"""
posts/123/comments/456/replies/789
posts/123/comments/456/comment_likes/789
"""
posts_comments_router = routers.NestedSimpleRouter(posts_router, r'comments', lookup='comment')
posts_comments_router.register(r'replies', ReplyViewSet)
posts_comments_router.register(r'comment_likes', CommentLikeViewSet)

"""
posts/12/comments/34/replies/56/reply_likes/78
"""
replies_likes_router = routers.NestedSimpleRouter(posts_comments_router, r'replies', lookup='reply')
replies_likes_router.register(r'reply_likes', ReplyLikeViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
    url(r'^', include(users_posts_router.urls)),
    url(r'^', include(posts_router.urls)),
    url(r'^', include(comments_router.urls)),
    url(r'^', include(posts_comments_router.urls)),
    url(r'^', include(replies_likes_router.urls)),
]