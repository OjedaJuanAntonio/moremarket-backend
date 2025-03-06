from django.contrib import admin
from .models import Auction, Bid

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'starting_price', 'start_time', 'end_time', 'created_by')
    search_fields = ('item_name', 'item_description', 'created_by__email')
    list_filter = ('start_time', 'end_time')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'auction', 'user', 'amount', 'created_at')
    search_fields = ('auction__item_name', 'user__email')
