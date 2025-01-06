from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import  permission_classes ,  throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import MenuItem, Category
from .models import  Cart ,  OrderItem, Order
from .serializers import MenuItemSerializer, ManagerSerializer, CategorySerializer , CategoryTitleSerializer
from .serializers import CartSerializer
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# Create your views here.
from .serializers import ListOrderSerializer, OrderItemSerializer, OrderSerializer, OrderDeliveryInfoSerializer
import datetime

@throttle_classes([AnonRateThrottle, UserRateThrottle])
class Categories(viewsets.ViewSet):
    def list(self,request):
        queryset = Category.objects.all()
        serialized = CategoryTitleSerializer(queryset, many=True)
        return Response({"Categories":serialized.data}, status=status.HTTP_200_OK)
    
    def create(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='manager').exists():
            serialized_item = CategorySerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        else:
             return Response({'message':'Vous naves l autorisation '},status.HTTP_401_UNAUTHORIZED)
    
    
@throttle_classes([AnonRateThrottle, UserRateThrottle])
class Menu_items(viewsets.ViewSet):
    def list(self, request):
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page', default=1)
        search = request.query_params.get('search')
        to_price=request.query_params.get('to_price')
        queryset = MenuItem.objects.select_related('category').all()    

        #price
        if to_price:
            queryset=queryset.filter(price__lte=to_price)
        #search
        if search:
            queryset = queryset.filter(title__icontains=search)
        #filtrage
        if ordering:
            queryset = queryset.order_by(ordering)
        #Pagination et page
        paginator = Paginator(queryset, per_page=perpage)
        try:
            queryset = paginator.page(number=page)
        except EmptyPage:
            queryset=[]
        #search

        serializer = MenuItemSerializer(queryset, many=True)
        return Response({"Menu ":serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='manager').exists():
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data, status.HTTP_201_CREATED)
        else:
             return Response({'message':'Vous naves l autorisation '},status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        if request.user.groups.filter(name='manager').exists():
            item = get_object_or_404(MenuItem, pk=pk)
            data = request.data
            item.title = data.get('title', item.title)
            item.price = data.get('price', item.price)
            item.featured = data.get('featured', item.featured)
            category_data = data.get('category')

            if category_data:
                category_id = category_data.get('slug')  # Supposons que la requête envoie l'ID de la catégorie
               
                item.category = get_object_or_404(Category,slug=category_id)

            item.save()  
            return Response({'message':'Element mis à jour '}, status.HTTP_200_OK)
        else:
            return Response({'message':'Vous naves l autorisation '},status.HTTP_401_UNAUTHORIZED)
    
         
    def partial_update(self, request, pk):
        if request.user.groups.filter(name='manager').exists():
            item = get_object_or_404(MenuItem, pk=pk)
            data = request.data
            if 'title' in data:
                item.title = data['title']
            
            if 'price' in data:
                item.price = data['price']
            
            if 'featured' in data:
                item.featured = data['featured']  
                
            if 'category' in data:
                category_id = data['category'].get('slug')  # Supposons que la requête envoie l'ID de la catégorie
                print(category_id)
                item.category = get_object_or_404(Category,slug=category_id)    
            item.save()
            return Response({'message':'Element partiellement mis à jour'}, status.HTTP_200_OK)
        else:
            return Response({'message':'Vous n etes pas autorisé'},status.HTTP_403_UNAUTHORIZED)
            
    def retrieve(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data, status.HTTP_200_OK)

    def destroy(self, request, pk):
        if request.users.group.filter(name='manager').exists():
            item = get_object_or_404(MenuItem, pk=pk)
            item.delete()
            return Response({"message: ": "Element supprimé"},status.HTTP_200_OK)
        else:
            return Response(status.HTTP_403_UNAUTHORIZED)
        
@permission_classes([IsAuthenticated])
class Manager(viewsets.ViewSet):
    def list(self, request):
        if request.user.is_superuser  or request.user.groups.filter(name='manager').exists():
            users = User.objects.filter(groups__name='manager')
            serialized = ManagerSerializer(users, many = True)
            return Response({'Managers':serialized.data}, status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_superuser  or request.user.groups.filter(name='manager').exists():
            userId = request.data.get('UserId')
            if userId:
                user = get_object_or_404(User, id=userId)
                
                managers = Group.objects.get(name='manager')
                managers.user_set.add(user)
                user.is_staff=True
                user.save()
                return Response({'message':'UserId '+str(userId)+ ' added'}, status.HTTP_200_OK)
            else:
                return Response({'message':'Entrer un identifiant valide'}, status.HTTP_200_OK)
        return Response({'message':'Vous navez pas l autorisation requise'}, status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, id):
        if request.user.is_superuser or request.user.groups.filter(name='manager').exists():
                user = get_object_or_404(User, id=id)
                managers = Group.objects.get(name='manager')
                managers.user_set.remove(user)
                return Response({'message':'UserId '+str(id)+ ' deleted from manager groups'}, status.HTTP_200_OK)
        return Response({'message':'Vous navez pas l autorisation requise'}, status.HTTP_403_UNAUTHORIZED)
    
class deliveryCrew(viewsets.ViewSet):
    def list(self, request):
        if request.user.is_superuser  or request.user.groups.filter(name='manager').exists():
            users = User.objects.filter(groups__name='delivery_crew')
            serialized = ManagerSerializer(users, many = True)
            return Response({'Delivery crew':serialized.data}, status.HTTP_200_OK)

    def create(self, request): 
        if request.user.groups.filter(name='manager').exists():
            userId = request.data.get('UserId')
            if userId :
                user = get_object_or_404(User, id=userId )
                delivery_crew= Group.objects.get(name='delivery_crew')
                delivery_crew.user_set.add(user)
                return Response({'message':'UserId '+userId+ ' added'}, status.HTTP_200_OK)
            else:
                return Response({'message':'Entrer un identifiant valide'}, status.HTTP_200_OK)
        return Response({'message':'Vous navez pas l autorisation requise'}, status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, id):
        if request.user.groups.filter(name='manager').exists():
                user = get_object_or_404(User, id=id)
                managers = Group.objects.get(name='delivery_crew')
                managers.user_set.remove(user)
                return Response({'message':'UserId '+str(id)+ ' deleted from delivery crew groups'}, status.HTTP_200_OK)
        return Response({'message':'Vous navez pas l autorisation requise'}, status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Cart.objects.filter(user=request.user)
        if  not queryset.exists():
            return Response({"Message ": "Aucun panier"}, status.HTTP_200_OK)

        else:
            print("Utilisateur: ", request.user)
            serialized = CartSerializer(queryset, many=True)
            return Response({"Cart elements: ": serialized.data}, status.HTTP_200_OK)
    
    def create(self, request):
        print("Request: ", request.data)
        serialized = CartSerializer(data=request.data,  context={'request': request})    
        serialized.is_valid(raise_exception=True)
        print(serialized)

        if not serialized.validated_data.get('user'):
            serialized.validated_data['user'] = request.user

        serialized.save()
        return Response({'message': 'ok'}, status.HTTP_200_OK)
        
       
    def destroy(self, request):
        queryset = Cart.objects.filter(user=request.user)

        if not queryset.exists():
            return Response({"Message":"No items to delete"}, status.HTTP_200_OK)
        else: 
            queryset.delete()

        return Response({"Message":"Cart items deleted"}, status.HTTP_200_OK)
        
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
class Orders(viewsets.ViewSet):
    def list(self, request):
        if request.user.groups.filter(name__in=['manager', 'delivery_crew']).exists():
            #For manager
            ordering = request.query_params.get('ordering')
            queryset1 = OrderItem.objects.select_related('user', 'menuitem').all()
            queryset2 = Order.objects.select_related('user').all()

            if ordering:
                queryset2 = queryset2.order_by(ordering)
        else:
            #For customers
            queryset1 = OrderItem.objects.select_related('user', 'menuitem').filter(user=request.user)
            queryset2 = Order.objects.select_related('user').filter(user=request.user)

        if not queryset1.exists():
            return Response({"Message": "Pas de commande en cours"}, status.HTTP_200_OK)
        else:
            serializer1 = ListOrderSerializer(queryset1, many=True)
            serializer2 = OrderDeliveryInfoSerializer(queryset2, many=True)
            return Response({"Commande": [serializer1.data, serializer2.data] }, status.HTTP_200_OK)         

    def create(self, request):
        #Customer
        #Recuperer le current cart
        cart_queryset = Cart.objects.filter(user=request.user)
        cart_serialized = CartSerializer(cart_queryset, many=True)

        #Remplir orderitemserializer model
        order_serialized= OrderItemSerializer(data= cart_serialized.data[0])
        print(order_serialized)
        order_serialized.is_valid(raise_exception=True)
        order_serialized.save()
        cart_queryset.delete()

        #Remplir orderserializer model
        commande = {
            'user' : cart_serialized.data[0]['user'],
            'delivery_crew': None,
            'status': 0,
            'total': cart_serialized.data[0]['price'],
            'date': datetime.date.today(),
        }
        commande_serialized = OrderSerializer(data=commande)
        print("Commande: ", order_serialized)
        commande_serialized.is_valid(raise_exception=True)
        commande_serialized.save()
        return Response({"Message": "Commande créé"}, status.HTTP_200_OK)
    
    def retrieve(self, request, id):
        param = {'id':id, 'user':request.user}
        queryset2 = Order.objects.select_related('user').filter(**param)
        if not queryset2:
            return Response({"Message":"Non autorisé"}, status.HTTP_200_OK)  
        queryset1 = OrderItem.objects.select_related('user', 'menuitem').filter(user=request.user)
        serializer1 = ListOrderSerializer(queryset1, many=True)
        return Response({"Id "+str(id): dict(serializer1.data[0] )}, status.HTTP_200_OK)         


    def update(self, request, id ):
        if request.user.groups.filter(name='manager').exists():    
            item = get_object_or_404(Order, id=id)
            data = request.data
            user_id = data.get('user')
            if user_id:   
                item.user = get_object_or_404(User,id=user_id)
            delivery_id = data.get('delivery_crew')
            if delivery_id:
                item.delivery_crew = get_object_or_404(User,id=delivery_id)
            item.status= data.get('status',  item.status)
            item.total= data.get('total',  item.total)
            item.date= data.get('date',  item.date)

            item.save()
            return Response({"Message": "Update effectué"}, status.HTTP_200_OK)
        else:
             return Response({"Message": "Authorisation requise"}, status.HTTP_200_OK)


    def partial_update(self, request, id):
        if request.user.groups.filter(name='manager').exists():
            item = get_object_or_404(Order, id=id)
            data = request.data
            if 'delivery_crew' in data:    
                delivery_id = data.get('delivery_crew')
                delivery_group = get_object_or_404(Group, name="delivery_crew")
                item.delivery_crew = get_object_or_404( User.objects.filter(groups=delivery_group),\
                                                       id=delivery_id)
                item.save()
                return Response({"Message": "Partial update effectué"}, status.HTTP_200_OK)
            if 'status' in data:   
                item.status= data.get('status', item.status)
                item.save()
               
                return Response({"Message": "Partial update effectué"}, status.HTTP_200_OK)         
                   
        elif request.user.groups.filter(name='delivery_crew').exists():
            item = get_object_or_404(Order, id=id)
            data = request.data
            if 'status' in data:   
                item.status= data.get('status', item.status)
                item.save()
                return Response({"Message": "Partial update effectué"}, status.HTTP_200_OK)
            else:
                return Response({"Message": "Vous ne pouvez pas effectué ces updates"}, status.HTTP_401_UNAUTHORIZED)
            
    def destroy(self, request, id):
        if request.user.groups.filter(name='manager').exists(): 
            queryset = Order.objects.filter(id=id)

        if not queryset.exists():
            return Response({"Message":"No items to delete"}, status.HTTP_200_OK)
        else: 
            queryset.delete()

        return Response({"Message":"Cart items deleted"}, status.HTTP_200_OK)
        






