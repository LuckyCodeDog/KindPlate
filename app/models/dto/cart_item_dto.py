class cart_item_dto:
    def __init__(self, menu_item_id: int, quantity: int, price: float, name: str, image_url: str = None):
        self.__menu_item_id = menu_item_id
        self.__name = name
        self.__quantity = quantity
        self.__price = price
        self.__image_url = image_url
    
    #generate getters and setters for the attributes
    @property
    def menu_item_id(self):
        return self.__menu_item_id  

    @property
    def quantity(self):
        return self.__quantity
    
    
    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self.__quantity = value
    
    
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self.__name = value
        
    @property
    def image_url(self):
        return self.__image_url
    
    @image_url.setter
    def image_url(self, value: str):
        if not value:
            raise ValueError("Image URL cannot be empty")
        self.__image_url = value 
           