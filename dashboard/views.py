# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser
# from gestionTienda.models import Order, Product
# from rest_framework.permissions import IsAuthenticated
# from gestionTienda.models import Order, Product, OrderItem
# from django.db.models import Sum, Q

# class AdminDashboardView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         # Métricas básicas
#         total_orders = Order.objects.count()
#         total_sales = Order.objects.aggregate(total=Sum('total'))['total'] or 0
#         pending_products = Product.objects.filter(is_approved=False).count()
        
#         data = {
#             "total_orders": total_orders,
#             "total_sales": str(total_sales),  # Convierte a string si es necesario
#             "pending_products": pending_products,
#         }
#         return Response(data)

# class VendedorDashboardView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Si no se pasa el parámetro 'seller', usamos el ID del usuario autenticado.
#         seller_id = request.query_params.get("seller") or request.user.id
#         try:
#             seller_id = int(seller_id)
#         except ValueError:
#             return Response({"error": "El parámetro 'seller' debe ser numérico."}, status=400)
        
#         # Total de pedidos: contamos las órdenes que contienen al menos un item de este vendedor.
#         total_orders = Order.objects.filter(
#             items__product__seller_id=seller_id
#         ).distinct().count()
        
#         # Ventas totales: sumamos el precio de cada OrderItem perteneciente a un producto del vendedor.
#         total_sales = OrderItem.objects.filter(
#             product__seller_id=seller_id
#         ).aggregate(total=Sum("price"))["total"] or 0
        
#         # Productos activos: cantidad de productos aprobados y con stock mayor a cero.
#         active_products = Product.objects.filter(
#             seller_id=seller_id, is_approved=True, stock__gt=0
#         ).count()
        
#         data = {
#             "total_orders": total_orders,
#             "total_sales": total_sales,
#             "active_products": active_products,
#         }
#         return Response(data)
