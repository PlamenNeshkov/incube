from django.conf import settings
from django.shortcuts import redirect

from rest_framework import mixins, status, viewsets, views, generics
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsUser
from users import models, serializers

import stripe, requests, urllib

class UserViewSet(mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, IsUser)

    def get_queryset(self):
        return self.request.user

    @list_route(methods=['get'])
    def profile(self, request):
        return Response(
            self.get_serializer(self.request.user).data,
            status=status.HTTP_200_OK
        )

    @list_route(methods=['get'])
    def stripe_authorize(self, request, pk=None):
        user = self.request.user
        if user.stripe_account:
            return Response(status=status.HTTP_403_FORBIDDEN)

        url = settings.STRIPE_CONNECT_HOST + settings.STRIPE_AUTHORIZE_PATH
        params = {
            'client_id': settings.STRIPE_CLIENT_ID,
            'response_type': 'code',
            'scope': 'read_write',
            'state': user.id
        }
        return redirect(url + '?' + urllib.parse.urlencode(params))

    @list_route(methods=['get'])
    def oauth_callback(self, request):
        self.permission_classes = (AllowAny,)

        url = settings.STRIPE_CONNECT_HOST + settings.STRIPE_TOKEN_PATH
        user = models.User.objects.get(id=request.query_params.get('state'))
        code = request.query_params.get('code')

        req_data = {
            'client_id': settings.STRIPE_CLIENT_ID,
            'client_secret': settings.STRIPE_SECRET_KEY,
            'code': code,
            'grant_type': 'authorization_code'
        }
        res = requests.post(url, json=req_data)
        data = res.json()

        stripe_account = models.StripeAccount.objects.create(
            stripe_id=data['stripe_user_id'],
            pub_key=data['stripe_publishable_key'],
            access_token=data['access_token'],
            refresh_token=data['refresh_token']
        )
        user.stripe_account = stripe_account
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateUserView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.CreateUserSerializer
    permission_classes = (AllowAny,)
