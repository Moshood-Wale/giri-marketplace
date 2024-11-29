from rest_framework import viewsets, filters, mixins, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Artisan, Product, Order
from .serializers import ArtisanSerializer, ProductSerializer, OrderSerializer, UserCreateSerializer, UserSerializer
from .permissions import IsArtisanOwnerOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema(
    tags=['authentication'],
    request=UserCreateSerializer,
    responses={
        201: OpenApiResponse(
            description="Successfully registered",
            response=UserSerializer
        ),
        400: OpenApiResponse(description="Bad request")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserCreateSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            
            return Response({
                'status': 'success',
                'message': 'User registered successfully',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(access),
                    }
                }
            }, status=status.HTTP_201_CREATED)
    except serializers.ValidationError as e:
        return Response({
            'status': 'error',
            'message': 'Validation error',
            'errors': e.detail
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['artisans'])
class ArtisanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['business_name', 'description', 'location']
    ordering_fields = ['business_name', 'created_at']

    def perform_create(self, serializer):
        # Check if user already has an artisan profile
        if Artisan.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("User already has an artisan profile")
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # For list view, show all artisans
        # For other operations, only show the user's artisan profile
        if self.action == 'list':
            return Artisan.objects.all()
        return Artisan.objects.filter(user=self.request.user)


@extend_schema(tags=['products'])
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsArtisanOwnerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['artisan', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']


@extend_schema(tags=['orders'])
class OrderViewSet(viewsets.GenericViewSet, 
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
