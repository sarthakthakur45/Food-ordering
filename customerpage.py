from DefaultPage import *
from Components.MessageComponent import WhiteMessage
from Components.ButtonComponent import *
from DatabaseHelper import *
from Components.table import SimpleTable
from PIL import Image,ImageTk
from tkinter import messagebox
from functools import reduce
import datetime

class CustomerHomePage(DefaultPage):
    def __init__(self,root,customer_details):
        super().__init__(root)
        #store customer details tuple here
        self.details=customer_details
        self.root.state('zoomed')
        #create dictionary for food menu items
        self.dct_IntVar = {}
        self.m=WhiteMessage(self.panel,text=f"Welcome {self.details[1]}")
        self.m.place(x=50, y=20)
        self.add_buttons()
        #Add the menu frame that has an image
        self.add_menu()

    def add_buttons(self):
        # Add 3 buttons- logout, check order status, order history
        self.logout=WhiteButton(self.f,text="Logout",command=self.customer_logout)
        self.logout.place(x=800, y=30)

        self.order_history_button=GrayButton(self.f,text="Check your order history",command=self.recent_orders)
        self.order_history_button.place(x=70,y=110)

        self.order_status_button=GrayButton(self.f,text="View Order Status",command=self.view_order_status)
        self.order_status_button.place(x=650,y=110)

    def customer_logout(self):
        import MainPage
        self.f.destroy()
        self.redirect=MainPage.MainPage(self.root)

    def recent_orders(self):
        query="""Select FoodDetails, FoodTotal,IsComplete,OrderDate
                from FoodOrder
                where CustomerId=%s
                order by FoodOrderId DESC"""
        parameters=(self.details[0],)
        result=DatabaseHelper.get_all_data(query,parameters)

        self.recent_orders_table = SimpleTable(self.f,rows=len(result),columns= len(result[0]), width=570, height=600)
        self.recent_orders_table.grid_propagate(0)
        self.recent_orders_table.place(x=30, y=170)
        for i in range(len(result)):
            for j in range(len(result[0])):
                if(j==0):
                    self.recent_orders_table.set(row=i,column=j,value=result[i][j],width=50)
                else:
                    self.recent_orders_table.set(row=i, column=j, value=result[i][j],width=10)


    def view_order_status(self):
        query="""
            Select FoodDetails,FoodTotal 
            from FoodOrder
            where CustomerId=%s
            and IsComplete=0
            order by FoodOrderId
        """
        parameters=(self.details[0],)

        result=DatabaseHelper.get_data(query,parameters)
        #Eg=("pizza,pasta",300)
        if(result is None):
            messagebox.showinfo("Orders complete","No orders pending")
        else:
            details = result[0]
            total = result[1]
            message = f"Currently preparing order for {details} and total amount {total}.Should be delivered soon"
            messagebox.showinfo("Order in progress", message)

    def add_menu(self):
        #  Add image, add 3 menu buttons
        # Add a button-> place order
        self.menu_frame=Frame(self.panel,height=600,width=600,bg="white")
        self.menu_frame.place(x=650,y=170)
        self.menu_frame.pack_propagate(0)

        self.raw_menu_image=Image.open("images/MenuBackground.jpg")
        self.raw_menu_image=self.raw_menu_image.resize((600,600))
        self.menu_img = ImageTk.PhotoImage(self.raw_menu_image)
        self.menu_panel = Label(self.menu_frame, image=self.menu_img)
        self.menu_panel.pack()

        self.food_menu_button=GrayButton(self.menu_frame,text="Food Menu",command=lambda : self.add_menu_items("Starters"))
        self.food_menu_button.place(x=30, y=550)

        self.drinks_menu_button=GrayButton(self.menu_frame,text="Drinks Menu",command=lambda : self.add_menu_items("Drinks"))
        self.drinks_menu_button.place(x=230, y=550)

        self.dessert_menu_button=GrayButton(self.menu_frame,text="Dessert Menu",command=lambda : self.add_menu_items("Desserts"))
        self.dessert_menu_button.place(x=430, y=550)

        self.place_order_button=GrayButton(self.f,text="Place Order",command=self.place_order)
        self.place_order_button.place(x=900,y=110)

    def place_order(self):
        selected_items=[]
        for key,item in self.dct_IntVar.items():
            if(item.get()==1):
                selected_items.append(key)

        if (len(selected_items) == 0):
            messagebox.showwarning("No order", "Please select atleast one food order to execute")

        else:
            query = """Select FoodName,FoodPrice
                            from FoodMenu
                            where FoodName in (%s)"""
            result=DatabaseHelper.get_all_data_multiple_input(query,selected_items)
            self.order_confirmation(result)

    def order_confirmation(self,result):
        print(f"Result is {result}")
        confirmation_window = Toplevel()
        confirmation_window.title('Confirm your order')
        f = SimpleTable(confirmation_window, rows=len(result), columns=len(result[0]),height=300, width=300)
        f.pack()

        for i in range(len(result)):
            for j in range(len(result[0])):
                f.set(row=i,column=j,value=result[i][j])

        b1 = Button(f, text="Confirm", height=2, width=10,command=lambda: self.send_order_to_admin(result, confirmation_window))
        b1.grid(row=len(result), column=0, padx=10, sticky='e')

        b2 = Button(f, text="Reset", height=2, width=10, command=lambda: self.reset_menu(confirmation_window))
        b2.grid(row=len(result), column=1, padx=10, sticky='w')

    def reset_menu(self,confirmation_window):
        confirmation_window.destroy()
        for key,value in self.dct_IntVar.items():
            if(value.get()==1):
                self.dct_IntVar[key].set(0)


    def send_order_to_admin(self,result,temp_window):
        temp_window.destroy()
        # result=(
        #     ('FoodName','FoodTotal'),
        #     ('Pizza',100),
        #     ('Coke', 200),
        #     ('Brownie', 225),
        # )
        print(f"Result is {result}")

        food_details=map(lambda x:x[0],result[1:])
        food_details=",".join(food_details)

        total_price=map(lambda x: x[1],result[1:])
        total_price=sum(total_price)

        print(food_details)
        print(total_price)

        query="""
        Insert into FoodOrder(CustomerId,FoodDetails,FoodTotal,OrderDate)
        Values(%s,%s,%s,%s)"""
        parameters=(self.details[0],food_details,total_price,datetime.datetime.today().date())
        DatabaseHelper.execute_query(query,parameters)
        message = f"Your order for {food_details} and total amount {total_price} is with us.Should be delivered soon"
        messagebox.showinfo("Order Placed", message)
















    def add_menu_items(self,food_type):
        query="""Select FoodMenuId,FoodName,FoodPrice
                from FoodMenu
                where FoodType=%s
        """
        parameters=(food_type,)
        result=DatabaseHelper.get_all_data(query,parameters)

        self.menu_items_frame = SimpleTable(self.menu_frame, rows=len(result),columns=len(result[0]),height=500, width=500)
        self.menu_items_frame.place(x=30, y=30)
        self.menu_items_frame.grid_propagate(0)
        self.text_font = ("MS Serif", 12)

        for i in range(1,len(result)):
            #Storing foodname as the key of dictionary
            self.dct_IntVar[result[i][1]]=IntVar()

        for i in range(len(result)):
            for j in range(len(result[0])):
                if(j==0 and i!=0):
                    c=Checkbutton(self.menu_items_frame,text=result[i][j],font=self.text_font,variable=self.dct_IntVar.get(result[i][1])) #to get FoodName
                    self.menu_items_frame.set(row=i, column=j, value=result[i][j],widget=c)
                else:
                    self.menu_items_frame.set(row=i,column=j,value=result[i][j],width=25)


if __name__ == '__main__':
    root=Tk()
    c=CustomerHomePage(root,(3,'Agicha',3,4))
    root.mainloop()


