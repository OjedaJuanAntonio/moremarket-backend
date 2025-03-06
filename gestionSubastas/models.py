from django.db import models
from django.utils.timezone import now
from django.conf import settings  # Para usar el modelo de usuario autenticado
from django.core.exceptions import ValidationError

class Auction(models.Model):
    item_name = models.CharField(max_length=255)  # Nombre del artículo
    item_description = models.TextField(default="Sin descripción", blank=True)  # Descripción del artículo
    # Se cambia de URLField a ImageField para manejo de imágenes; se guardarán en MEDIA_ROOT/auctions/
    item_image = models.ImageField(upload_to='auctions/', blank=True, null=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio inicial
    start_time = models.DateTimeField()  # Fecha y hora de inicio
    end_time = models.DateTimeField()  # Fecha y hora de finalización
    # Se elimina el campo is_active
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auctions"
    )

    def __str__(self):
        return f"Subasta: {self.item_name} creada por {self.created_by.username}"

    def clean(self):
        # Validar que la fecha de inicio sea anterior a la fecha de finalización.
        if self.start_time >= self.end_time:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de finalización.")

    def get_highest_bid(self):
        return self.bids.order_by('-amount').first()
    
    def get_status(self):
        """
        Devuelve el estado de la subasta según las fechas:
          - "Próxima": Si el tiempo actual es anterior a start_time.
          - "Activa": Si start_time es menor o igual que ahora y ahora es menor que end_time.
          - "Finalizada": Si el tiempo actual es mayor o igual a end_time.
        """
        current_time = now()
        if current_time < self.start_time:
            return "Próxima"
        elif self.start_time <= current_time < self.end_time:
            return "Activa"
        else:
            return "Finalizada"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad de la puja
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la puja

    def __str__(self):
        return f"Puja de {self.user.username} por {self.amount} en {self.auction.item_name}"

    def clean(self):
        highest_bid = self.auction.get_highest_bid()
        if highest_bid and self.amount <= highest_bid.amount:
            raise ValidationError("La cantidad de la puja debe ser mayor que la puja más alta actual.")
