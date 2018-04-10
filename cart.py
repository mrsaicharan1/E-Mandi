class ShoppingCart():
 
    def __init__(self):
        self.total = 0
        self.items = dict()
 
    def add_item(self,item_name,quantity,price):

        self.total = float(self.total) + float(price*quantity)
        self.items[item_name] = quantity
 
    def remove_item(self,item_name,quantity,price):
        
        # get remaining quantity of item to be removed in items
        quantityLeft = self.items[item_name]
 
        #checkk if its greater than the quantity to be removed
        if quantityLeft > quantity:
            #reduce the quantity
            self.items[item_name] = self.items[item_name]  - quantity            
            #reduce the total cost
            self.total = self.total - (price*quantity)        
        else:
            #assume the item is nolonger needed, delete it from items
            self.total = self.total - (price*quantityLeft) 
            self.items.pop(item_name)
 
    def checkout(self,cash_paid):
        """ return the customer's balance"""
        #if cash paid is less than total
        if cash_paid < self.total:
            return "Cash paid not enough"
        else:
            return cash_paid - self.total