# from django.db import models
# from django.utils.timezone import now
# from django.conf import settings  # Para usar el modelo de usuario autenticado
# from django.core.exceptions import ValidationError


# class Auction(models.Model):
#     item_name = models.CharField(max_length=255)  # Nombre del artículo
#     item_description = models.TextField(default="Sin descripción", blank=True)  # Descripción del artículo
#     item_image = models.URLField(max_length=500, blank=True, null=True)  # Imagen del artículo
#     starting_price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio inicial
#     start_time = models.DateTimeField()  # Fecha y hora de inicio
#     end_time = models.DateTimeField()  # Fecha y hora de finalización
#     is_active = models.BooleanField(default=True)  # Indica si la subasta está activa
#     created_by = models.ForeignKey(  # Usuario que creó la subasta
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="auctions"
#     )

#     def __str__(self):
#         return f"Subasta: {self.item_name} creada por {self.created_by.username}"

#     def clean(self):
#         # Validación: la fecha de inicio debe ser anterior a la fecha de finalización
#         if self.start_time >= self.end_time:
#             raise ValidationError("La fecha de inicio debe ser anterior a la fecha de finalización.")
#         # Validación: la subasta no debe empezar en el pasado
#         if self.start_time < now():
#             raise ValidationError("La fecha de inicio no puede estar en el pasado.")

#     def get_highest_bid(self):
#         # Obtiene la puja más alta de la subasta
#         return self.bids.order_by('-amount').first()


# class Bid(models.Model):
#     auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
#     user = models.ForeignKey(  # Usuario autenticado que realizó la puja
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="bids"
#     )
#     amount = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad de la puja
#     created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la puja

#     def __str__(self):
#         return f"Puja de {self.user.username} por {self.amount} en {self.auction.item_name}"

#     def clean(self):
#         # Validación: la puja debe ser mayor que la más alta existente
#         highest_bid = self.auction.get_highest_bid()
#         if highest_bid and self.amount <= highest_bid.amount:
#             raise ValidationError("La cantidad de la puja debe ser mayor que la puja más alta actual.")



from django.db import models
from django.utils.timezone import now
from django.conf import settings  # Para usar el modelo de usuario autenticado
from django.core.exceptions import ValidationError


class Auction(models.Model):
    item_name = models.CharField(max_length=255)  # Nombre del artículo
    item_description = models.TextField(default="Sin descripción", blank=True)  # Descripción del artículo
    item_image = models.URLField(max_length=500, blank=True, null=True)  # Imagen del artículo
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio inicial
    start_time = models.DateTimeField()  # Fecha y hora de inicio
    end_time = models.DateTimeField()  # Fecha y hora de finalización
    is_active = models.BooleanField(default=True)  # Indica si la subasta está activa
    created_by = models.ForeignKey(  # Usuario que creó la subasta
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auctions"
    )

    def __str__(self):
        return f"Subasta: {self.item_name} creada por {self.created_by.username}"

    def clean(self):
        # Validación: la fecha de inicio debe ser anterior a la fecha de finalización
        if self.start_time >= self.end_time:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de finalización.")
        # Validación: la subasta no debe empezar en el pasado
        if self.start_time < now():
            raise ValidationError("La fecha de inicio no puede estar en el pasado.")

    def get_highest_bid(self):
        # Obtiene la puja más alta de la subasta
        return self.bids.order_by('-amount').first()


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(  # Usuario autenticado que realizó la puja
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad de la puja
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de la puja

    def __str__(self):
        return f"Puja de {self.user.username} por {self.amount} en {self.auction.item_name}"

    def clean(self):
        # Validación: la puja debe ser mayor que la más alta existente
        highest_bid = self.auction.get_highest_bid()
        if highest_bid and self.amount <= highest_bid.amount:
            raise ValidationError("La cantidad de la puja debe ser mayor que la puja más alta actual.")
