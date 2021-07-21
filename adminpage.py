from DefaultPage import *
from Components.ButtonComponent import WhiteButton
from DatabaseHelper import *
from Components.table import SimpleTable
from Components.MessageComponent import WhiteMessage
from tkinter import messagebox
class AdminHomePage(DefaultPage):
    def __init__(self,root,admin_details):
        print("Admin home page called")
        super().__init__(root)
        self.root.state('zoomed')# Maximize the screen
        #Tuple received from DATABASE. Eg=> (2, 'Ritesh', 'SGT', 'riteshagicha@gmail.com', 'RiteshPic3.jpg')
        self.details=admin_details
        #Dictionary to store the pending order checkbox IntVars
        self.dct_IntVar={}

        self.admin_page = WhiteMessage(self.f, text="Admin Page")
        self.admin_page.place(x=320, y=20)
        self.add_admin_details()
        self.add_buttons()

    def add_admin_details(self):
        # Add image of admin
        # Add Name of admin as Message
        # Add email of admin as Message
        print(self.details)
        self.admin_raw_image=Image.open('images/'+self.details[4])
        self.admin_raw_image.resize((100,180))
        self.profile_pic = ImageTk.PhotoImage(self.admin_raw_image)
        #ensure this size is same as image size, also we can use label instead of this
        self.c=Canvas(self.f,width=100,height=180)
        # give the starting cordinates wrt canvas i.e 0,0
        self.canvas_pic=self.c.create_image(0,0,image=self.profile_pic,anchor=NW)
        self.c.place(x=40,y=100)
        #message that displays admin's name
        self.admin_name = WhiteMessage(self.f,text="Name= "+self.details[1],width=200)
        self.admin_name.place(x=40, y=300)
        #message that displays admin's email address
        self.admin_email = WhiteMessage(self.f, text="Email "+self.details[3], width=300)
        self.admin_email.place(x=40, y=350)

    def add_buttons(self):
        #Add 3 buttons
        # View pending order
        #View recently completed order
        #logout

        # doesn't matter, you can add to the frame or panel(Label- for image)
        self.pending_button = WhiteButton(self.f, "View Pending Orders", self.view_pending_orders)
        self.pending_button.place(x=400, y=90)
        self.completed_button = WhiteButton(self.f, "View Recent Completed Orders", self.view_completed_orders)
        self.completed_button.place(x=600, y=90)
        self.logout = WhiteButton(self.f, "Logout", self.admin_logout, width=10)
        self.logout.place(x=800, y=20)

    def view_completed_orders(self):
        #same as pending orders, only diff is we dont need checkbutton here
        query="""select FoodOrderId,CustomerName,FoodDetails,FoodTotal,OrderDate
                from FoodOrder fo
                join Customer c on fo.CustomerId=c.CustomerID
                where IsComplete=1
                order by FoodOrderId desc LIMIT 10"""
        result=DatabaseHelper.get_all_data(query)
        self.menu_frame = SimpleTable(self.f, rows=len(result),columns=len(result[0]),height=500, width=660)
        self.menu_frame.place(x=500, y=200)
        self.menu_frame.grid_propagate(0)

        for i in range(len(result)):
            for j in range(len(result[0])):
                self.menu_frame.set(row=i,column=j,value=result[i][j])

    def execute_order(self):
        selected_items = []
        for key,value in self.dct_IntVar.items():
            if(value.get()==1):
                selected_items.append(key)
                self.dct_IntVar[key].set(0)
        print(selected_items)
        if(len(selected_items)==0):
            messagebox.showwarning("No order", "Please select atleast one food order to execute")
        else:
            query="""Update world.FoodOrder 
                    Set IsComplete=1
                    where FoodOrderId in (%s)"""
            DatabaseHelper.execute_all_data_multiple_input(query,selected_items)
            messagebox.showinfo("Success",f"Order Id(s) {selected_items} executed")
            self.view_pending_orders()


    def view_pending_orders(self):
        #Add execute button
        #Add table that shows pending orders with checkbutton
        self.execute_button=WhiteButton(self.f,"Execute Order",self.execute_order)
        self.execute_button.place(x=500,y=150)
        query="""select FoodOrderId,CustomerName,FoodDetails,FoodTotal,OrderDate
                from Customer c 
                join FoodOrder fo 
                on c.CustomerId=fo.CustomerId
                where fo.IsComplete=0 """
        result=DatabaseHelper.get_all_data(query)
        print(result)

        self.menu_frame = SimpleTable(self.f, rows=len(result),columns=len(result[0]),height=500, width=650)
        self.menu_frame.place(x=500, y=200)
        self.menu_frame.grid_propagate(0)
        self.text_font = ("MS Serif", 12)

        for i in range(1,len(result)):
            #store FoodOrderID as key and a checkbutton variable as value
            self.dct_IntVar[result[i][0]]=IntVar()

        for i in range(len(result)):
            for j in range(len(result[0])):
                if(j==0 and i!=0):
                #Put checkbutton in the all first column apart from the first row
                    c=Checkbutton(self.menu_frame,text=result[i][j],font=self.text_font,variable=self.dct_IntVar.get(result[i][j]))
                    self.menu_frame.set(row=i, column=j, value=result[i][j],widget=c)
                else:
                    self.menu_frame.set(row=i,column=j,value=result[i][j])

    def admin_logout(self):
        import MainPage
        self.f.destroy()
        self.panel.destroy()
        self.redirect=MainPage.MainPage(self.root)


if(__name__=="__main__"):
    root=Tk()
    admin_details=(2, 'Ritesh', 'SGT', 'riteshagicha@gmail.com', 'RiteshPic3.jpg')
    a=AdminHomePage(root,admin_details)
    root.mainloop()