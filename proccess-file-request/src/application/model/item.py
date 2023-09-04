class Item:
    def __init__(self, site, id, price, start_time, category_name, currency_description, seller_nickname):
        self.site = site
        self.id = id
        self.price = price
        self.start_time = start_time
        self.category_name = category_name
        self.currency_description = currency_description
        self.seller_nickname = seller_nickname

    def key(self):
        return self.site + str(self.id)

    def getValues(self):
        return (self.site, self.id, self.price, self.start_time, self.category_name, self.currency_description, self.seller_nickname)