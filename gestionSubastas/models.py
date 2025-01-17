# # gestionSubastas/models.py
# from django.db import models
# from gestionTienda.models import Product
# from django.contrib.auth.models import User

# class Auction(models.Model):
#     product = models.OneToOneField(Product, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Auction for {self.product.name}"

# class Bid(models.Model):
#     auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Se asocia con el usuario autenticado
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Puja de {self.user.username} por {self.amount} en {self.auction.product.name}"

# gestionSubastas/models.py
from django.db import models
from gestionTienda.models import Product
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.conf import settings  # Importa settings


class Auction(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Auction for {self.product.name}"

    def clean(self):
        # Validación: La fecha de inicio debe ser anterior a la fecha de fin
        if self.start_time >= self.end_time:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")

    def place_bid(self, user, amount):
        if not self.is_active or now() > self.end_time:
            raise ValidationError("La subasta ya ha terminado.")
        highest_bid = self.get_highest_bid()
        if highest_bid and amount <= highest_bid.amount:
            raise ValidationError("La puja debe ser mayor que la puja más alta actual.")
        Bid.objects.create(auction=self, user=user, amount=amount)

    def get_highest_bid(self):
        return self.bids.order_by('-amount').first()


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Usa la referencia al modelo personalizado
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Puja de {self.user.username} por {self.amount} en {self.auction.product.name}"
