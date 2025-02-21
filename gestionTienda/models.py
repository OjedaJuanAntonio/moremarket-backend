from django.db import models
from django.conf import settings

# Categorías de productos
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

# Producto con variantes y stock
class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)  # Control de aprobación
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

# Producto con variantes (ej. tallas, colores)
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=100)  # Ej: "Talla", "Color"
    variant_value = models.CharField(max_length=100)  # Ej: "M", "Rojo"
    extra_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ('product', 'variant_name', 'variant_value')
    
    def __str__(self):
        return f"{self.product.name} - {self.variant_name}: {self.variant_value}"

# Reseñas y calificaciones para productos
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # Ej: 1 a 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reseña de {self.user.email} para {self.product.name}"

# Pedido y detalle del pedido (Order y OrderItem)
class Order(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="Pendiente")  # Ej: Pendiente, Pagado, Enviado, Cancelado
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido {self.id} de {self.buyer.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario en el momento de la compra
    
    def __str__(self):
        product_name = self.product.name if self.product else "Producto eliminado"
        return f"{self.quantity} x {product_name}"
