Create Table FoodOrder
(
	FoodOrderId int auto_increment key,
    CustomerId int,
    FoodDetails varchar(1000),
    FoodTotal int,
    IsComplete int default 0,
    OrderDate DATE
)
