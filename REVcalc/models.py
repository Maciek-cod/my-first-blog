from django.db import models
from django.contrib.auth.models import AbstractUser
from dateutil import parser
import requests
from datetime import timedelta


class User(AbstractUser):
    pass


class Document(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="usery")
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model): 
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="buyuser")
    file_name = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.CharField(max_length=200)
    currency = models.CharField(max_length=50)
    trade_date = models.DateTimeField(default='01/01/2020')
    settle_date = models.DateTimeField(default='01/01/2020')
    total = models.CharField(max_length=200)
    line = models.CharField(max_length=200)
    quantity_after_transaction = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "ID: "+ str(self.id) +" Code: "+ self.name +" Quantity: "+ str(self.quantity)

    def quantity_abs(self):
        return abs(self.quantity)

    def profit(self):
        total = 0
        for sell_detail in self.sold.all():
            total += sell_detail.profit
        return total

    @classmethod
    def load_from_revolut_txt(cls, file, user):
        f = open("media/"+file.name, "r")
        lines  = f.readlines()
        for stock in lines:
            field_list = stock.split()
            trade_date = field_list[0]
            settle_date = field_list[1]
            currency = field_list[2]
            type = field_list[3]
            name = field_list[4]
            quantity = field_list[-3]
            price = field_list[-2]
            total = field_list[-1]
            
            if type == "BUY" or type == "SELL":

                Transaction.objects.create(
                    user=user, file_name=file.name, name=name, type=type, 
                    quantity=quantity ,price=price, currency=currency, 
                    trade_date=parser.parse(trade_date), 
                    settle_date=parser.parse(settle_date), total=total, line=stock)

    @classmethod
    def update_quantity_after_transaction(cls, user):
        user_transactions = Transaction.objects.filter(user=user).order_by('name','settle_date')
        balance = 0
        name = ""

        for transaction in user_transactions:
            if name == "":
                balance = transaction.quantity
                name = transaction.name
            elif name == transaction.name:
                if transaction.type == "BUY":
                    balance += transaction.quantity
                if transaction.type == "SELL":
                    balance = balance - abs(transaction.quantity)
            else:
                name = transaction.name
                balance = transaction.quantity
            Transaction.objects.filter(id=transaction.id).update(quantity_after_transaction=balance)
            

class Sell_detail(models.Model):
    sell = models.ForeignKey("Transaction", on_delete=models.CASCADE, related_name="sold")
    buy = models.ForeignKey("Transaction", on_delete=models.CASCADE, related_name="bought")
    quantity = models.IntegerField()
    qty_stayed = models.IntegerField()
    sell_left = models.IntegerField(default=0)
    profit = models.FloatField(default=0)
    profit_pln = models.FloatField(default=0)
    
    @classmethod
    def create_sell_details(cls,file, user):

        """ Adds sell detail object to model for reporting profit and tax """

        sell_stock = Transaction.objects.filter(user=user, file_name=file, type="SELL").order_by('name','settle_date')
        for sell_stock in sell_stock:
            rate = Rate.objects.get(date=sell_stock.settle_date.date())
            sell_stock_pln = float(sell_stock.price) * rate.pln
            buy_stock = Transaction.objects.filter(user=user, name=sell_stock.name, type="BUY").order_by('settle_date')
            for buy_stock in buy_stock:
                if buy_stock.active == True:
                    rate = Rate.objects.get(date=buy_stock.settle_date.date())
                    buy_stock_pln = float(buy_stock.price) * rate.pln
                    buy_quantity = Sell_detail.count_buy_stocks_quantity(buy_stock)
                    selling_qnty = Sell_detail.count_sell_stocks_quantity(sell_stock)
                    
                    if selling_qnty > buy_quantity:

                        quantity = buy_quantity 
                        qty_stayed = 0
                        sell_left = selling_qnty - buy_quantity
                        diffrence = float(sell_stock.price) - float(buy_stock.price)
                        profit = diffrence * quantity
                        diffrence_pln = float(sell_stock_pln) - float(buy_stock_pln)
                        profit_pln = diffrence_pln * quantity
                        Sell_detail.objects.create(sell=sell_stock, buy=buy_stock, quantity=quantity, qty_stayed=qty_stayed, sell_left=sell_left, profit=profit, profit_pln=profit_pln)
                        buy_stock.active = False
                        buy_stock.save()

                    elif selling_qnty < buy_quantity: 

                        quantity = selling_qnty 
                        qty_stayed = buy_quantity - quantity
                        diffrence = abs(float(sell_stock.price)) - float(buy_stock.price)
                        profit = diffrence * quantity
                        diffrence_pln = float(sell_stock_pln) - float(buy_stock_pln)
                        profit_pln = diffrence_pln * quantity
                        Sell_detail.objects.create(sell=sell_stock, buy=buy_stock, quantity=quantity, qty_stayed=qty_stayed, profit=profit, profit_pln=profit_pln)
                        break

                    else:
                        quantity = buy_quantity
                        qty_stayed = 0
                        diffrence = abs(float(sell_stock.price)) - float(buy_stock.price)
                        profit = diffrence * quantity
                        diffrence_pln = float(sell_stock_pln) - float(buy_stock_pln)
                        profit_pln = diffrence_pln * quantity
                        Sell_detail.objects.create(sell=sell_stock, buy=buy_stock, quantity=quantity, qty_stayed=qty_stayed, profit=profit, profit_pln=profit_pln)
                        buy_stock.active = False
                        buy_stock.save()
                        break

    @classmethod
    def count_buy_stocks_quantity(cls, buy_stock):
        if Sell_detail.objects.filter(buy=buy_stock).exists():
            buy_transactions = Sell_detail.objects.filter(buy=buy_stock)
            buy_quantity = 0 
            for buy_transaction in buy_transactions:
                if buy_transaction.qty_stayed != 0:
                    buy_quantity += buy_transaction.qty_stayed
                else:
                    buy_quantity = buy_stock.quantity
        else:
            buy_quantity = buy_stock.quantity
        return buy_quantity

    @classmethod
    def count_sell_stocks_quantity(cls, sell_stock):
        if Sell_detail.objects.filter(sell=sell_stock).exists():
           sells_left = Sell_detail.objects.filter(sell=sell_stock).order_by('id')
           for sell_left in sells_left:
               sell_left = sell_left.sell_left
           print(sell_left)
        else:
            sell_left = sell_stock.quantity_abs()
        return sell_left

class Rate(models.Model):
    date = models.DateTimeField(default='01/01/2020')
    pln = models.FloatField(default=0)

    @classmethod
    def create_pln_rate(cls, user):
        stocks = Transaction.objects.filter(user=user).order_by('settle_date')
        for stock in stocks:
            if not Rate.objects.filter(date=stock.settle_date.date()).exists():
                url_template = "http://api.nbp.pl/api/exchangerates/rates/a/usd/{}".format(stock.settle_date.date())
                while True:
                    x = requests.get(url_template.format('USD'))
                    if x:
                        break 
                    else:
                        yesterday = stock.settle_date.date() - timedelta(days=1)
                        data_str = yesterday.strftime("%Y-%m-%d")
                        url_template = "http://api.nbp.pl/api/exchangerates/rates/a/usd/{}".format(data_str)
                        x = requests.get(url_template.format('USD')) 

                pln_rate = requests.get(url_template.format('USD')).json()["rates"][0]["mid"]
                Rate.objects.create(date=stock.settle_date.date(), pln=pln_rate)