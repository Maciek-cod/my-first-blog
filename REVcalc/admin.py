from django.contrib import admin
from .models import Sell_detail, User, Document, Transaction, Rate

# Register your models here.
admin.site.register(User)
admin.site.register(Document)
admin.site.register(Rate)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'settle_date', 'name', 'type', 'quantity', 'price')
    ordering = ('user', 'name','settle_date',)
    list_filter = ('user',)

class Sell_detailAdmin(admin.ModelAdmin):
    list_display = ('id','buy', 'sell',  'quantity', 'qty_stayed', 'profit', 'profit_pln')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Sell_detail, Sell_detailAdmin)