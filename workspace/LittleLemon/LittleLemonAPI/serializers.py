from rest_framework import serializers 
from .models import MenuItem
from .models import Category
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import  Cart, Order, OrderItem

class CategoryTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields=[ 'title']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields=['slug', 'title']
        #fields = ['id']

class MenuItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    featured = serializers.BooleanField()
    category = CategorySerializer()

    class Meta:
        model= MenuItem
        fields=['title','price','featured', 'category', 'id']

    def create(self, validated_data):
        # Extraire les données de la catégorie
        category_data = validated_data.pop('category')

        # Créer ou récupérer la catégorie correspondante
        category, _ = Category.objects.get_or_create(**category_data)

        # Créer le MenuItem avec la catégorie associée
        menu_item = MenuItem.objects.create(category=category, **validated_data)
        return menu_item
    
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault(),
        
    )
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset = MenuItem.objects.all(),
    )
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.SerializerMethodField(method_name='calculate_price', read_only=True)
    class Meta:
        model = Cart
        fields = ['user','price', 'quantity',  'unit_price',  'menuitem']
        read_only_fields = ['user','price' ] 
    
    def calculate_price(self, p:Cart):
        return p.quantity * p.unit_price


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault(),
    )
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault(),
        allow_null=True,
    )
    status = serializers.BooleanField( default=0)
    total = serializers.DecimalField(max_digits=6, decimal_places=2)
    date = serializers.DateField()

    class Meta:
        model=Order
        fields=['user', 'delivery_crew', 'status', 'total', 'date']
        

class OrderItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault(),
    )
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), 
    )
    quantity = serializers.IntegerField(default=0)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderDeliveryInfoSerializer(serializers.ModelSerializer):
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault(),
        allow_null=True,
    )
    status = serializers.BooleanField( default=0)
    date = serializers.DateField()

    class Meta:
        model=Order
        fields=['delivery_crew', 'status',  'date', 'id']

class ListOrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        default=serializers.CurrentUserDefault(),
    )
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), 
    )
    quantity = serializers.IntegerField(default=0)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    #delivery_info = OrderDeliveryInfoSerializer(source='user',  read_only=True )

    class Meta:
        model = OrderItem
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']









    

