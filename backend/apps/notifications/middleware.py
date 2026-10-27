"""JWT authentication middleware for Channels WebSocket connections.

The SPA authenticates with JWTs (not Django sessions), so the WebSocket must
authenticate from a ``?token=<access>`` query-string parameter rather than a
session cookie.
"""
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def _get_user(validated_token):
    from rest_framework_simplejwt.authentication import JWTAuthentication
    try:
        return JWTAuthentication().get_user(validated_token)
    except Exception:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from rest_framework_simplejwt.tokens import AccessToken

        query_string = scope.get('query_string', b'').decode()
        token = parse_qs(query_string).get('token', [None])[0]

        scope['user'] = AnonymousUser()
        if token:
            try:
                validated = AccessToken(token)
                scope['user'] = await _get_user(validated)
            except Exception:
                scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
