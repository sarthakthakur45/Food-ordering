Create table FoodMenu
(
	FoodMenuId int auto_increment key,
    FoodName 	varchar(100),
    FoodPrice	int,
    FoodType	varchar(100)
)


--FOOD
Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Pizza',350,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Cheese Pizza',450,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Farmhouse Pizza',600,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Veggie overload Pizza',750,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Burger',200,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Cheese Burger',250,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Jumbo Burger',350,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Alfredo Pasta',300,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Chunky Basil Pasta',350,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Regular Fries',150,'Starters');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Peri Peri Fries',200,'Starters');

--DRINKS
Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Pineapple',150,'Drinks');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Lemon',150,'Drinks');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Apple',150,'Drinks');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Coke',100,'Drinks');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Sprite',100,'Drinks');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Mango',150,'Drinks');

--DESSERT
Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Sizzling brownie',200,'Desserts');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Vanilla',150,'Desserts');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Waffles',200,'Desserts');

Insert into FoodMenu(FoodName,FoodPrice,FoodType)
values('Triple trouble',250,'Desserts');
