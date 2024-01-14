from bs4 import BeautifulSoup
import requests
from tkinter import *
from datetime import timedelta, date

DCdict = {1: 'Carillo', 2: 'De La Guerra', 3: 'Ortega', 4: 'Portola'}
Mealdict = {0: 'Brunch', 1: 'Breakfast', 2: 'Lunch', 3: 'Dinner'}
Parameters = [] #for calling gradMenus
today = str(date.today())
Parameters = [today, 3]
all_dishes_list = []
widgets_list = []

#widget object
window = Tk()

#list of starred foods
favFoods = []

#create array of 7 days
date_string_list = []

#initialize data_string_list
for i in range(7):
    day = date.today() + timedelta(days=i)
    string = str(day)
    print(string)
    date_string_list.append(string)

#meal and date selection frame 
topFrame = Frame(window, width=100, height=3, bg='white')
topFrame.grid(row = 0, column = 0)

#dining common title frame
bottomFrame = Frame(window, width=100, height=3, bg='grey')
bottomFrame.grid(row = 1, column = 0)

#list of foods frame
listFrame = Frame(window, width=100, height = 3, bg = 'grey')
listFrame.grid(row = 2, column = 0)

#object for toggle button for meal selection
class meals(Button):
    registry = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command = self.click_function)
        self.registry.append(self)
        self.ID = -1
    def set_ID(self, val):
        self.ID = val
    def click_function(self):
        if self.config('relief')[-1] == 'sunken':
            self.config(relief="raised")
            self.config(bg = "white")
            Parameters[1] = -1
        else:
            self.config(relief="sunken")
            self.config(bg = "#717171")
            Parameters[1] = self.ID
            for meal in self.registry:
                if meal != self:
                    print(meal)
                    meal.config(relief="raised")
                    meal.config(bg = "white")
    

#object for toggle button for date selection
class dates(Button):
    registry = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command = self.click_function)
        self.registry.append(self)
        self.ID = ""
    def set_ID(self, val):
        self.ID = val
    def click_function(self):
        if self.config('relief')[-1] == 'sunken':
            self.config(relief="raised")
            self.config(bg = "white")
            Parameters[0] = ""
        else:
            self.config(relief="sunken")
            self.config(bg = "#717171")
            Parameters[0] = self.ID
            for date in self.registry:
                if date != self:
                    print(date)
                    date.config(relief="raised")
                    date.config(bg = "white")

#object for toggle button for star button
class star(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command = self.click_function)
    def click_function(self):
        x, y = self.grid_info()["column"], self.grid_info()["row"]
        food = listFrame.grid_slaves(y, x-1)[0]['text']
        if self.config('relief')[-1] == 'sunken':
            self.config(relief="raised")
            self.config(bg = "white")
            if food in favFoods:
                favFoods.remove(food)
        else:
            self.config(relief="sunken")
            self.config(bg = "gold")
            if food not in favFoods:
                favFoods.append(food)
        print(x, y)
        print(favFoods)

#meal selection buttons  

# format of the url: 
# https://apps.dining.ucsb.edu/menu/day?dc=carrillo&d=2024-01-13&m=breakfast&m=brunch&m=lunch&m=dinner&m=late-night&food=

def generateURL(date, diningHall, meal):
    url = "https://apps.dining.ucsb.edu/menu/day?dc="
    if(diningHall == 1):
        url += "carrillo"
    elif(diningHall == 2):
        url += "de-la-guerra"
    elif(diningHall == 3):
        url += "ortega"
    elif(diningHall == 4):
        url += "portola"
    url += "&d=" + date + "&"
    if(meal == 0):
        url += "m=brunch"
    elif(meal == 1):
        url += "m=breakfast"
    elif(meal == 2):
        url += "m=lunch"
    elif(meal == 3):
        url += "m=dinner"
    return url

def grabMenus(Para, Printable = False):
    if(Parameters[1] == -1 or Parameters[0] == ""):
        return [["bruh", "bruh", "bruh", "bruh"], ["bruh", "bruh", "bruh", "bruh"], ["bruh", "bruh", "bruh", "bruh"], ["bruh", "bruh", "bruh", "bruh"]]
    all_dishes_list = [[], [], [], []]
    day = Para[0]
    meal = Para[1]
    for dc in range(1, 5):
        url = generateURL(day, dc, meal)
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
            #print(url)
        for dish in soup.find_all('dd'):
            item = str(dish)
            item = item[4 : (len(item) - 5)]
            index = item.find('&')
            if(index > 0):
                item = item[0, index] + item[item.find('&')]
            all_dishes_list[dc - 1].append(item)
    if(Printable):
        for dc in range(1, 5):
            print("-------------" + DCdict[dc] + "-------------")
            if(not all_dishes_list[dc - 1]):
                continue
            print("-------------" + Mealdict[meal] + "-------------")
            for dish in all_dishes_list[dc - 1]:
                print(dish)
    return all_dishes_list

def grabAllMenusFromOneDay(date, printable = False):
    all_dishes_list = [[[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []]]
    for dc in range(1, 5):
        for meal in range(0, 4):
            url = generateURL(date, dc, meal)
            req = requests.get(url) 
            soup = BeautifulSoup(req.content, "html.parser")
            #print(url)
            for dish in soup.find_all('dd'):
                item = str(dish)
                item = item[4 : (len(item) - 5)]
                all_dishes_list[dc - 1][meal].append(item)
    if(printable):
        for dc in range(1, 5):
            print("-------------" + DCdict[dc] + "-------------")
            for meal in range(0, 4):
                if(not all_dishes_list[dc - 1][meal]):
                    continue
                print("-------------" + Mealdict[meal] + "-------------")
                for dish in all_dishes_list[dc - 1][meal]:
                    print(dish)
    return all_dishes_list; 

def printAllDishes(all_dishes_list):
    for dc in all_dishes_list:
        for meal in dc: 
            for dish in meal:
                print(dish)

def generateMenu(menu, col):
    if(len(menu) == 0):
        food = Label(listFrame,
                        text = "Food is not available here",
                        width = 30,
                        pady = 5).grid(row = 1,
                                        column = col)
        for i in range(1,26):
            food = Label(listFrame,
                            text = "",
                            width = 30,
                            pady = 5).grid(row = i+1,
                                            column = col)
    for i in range(len(menu)):
        food = Label(listFrame,
                        text = menu[i],
                        width = 29,
                        pady = 5).grid(row = i+1,
                                        column = col)
        Button = star(listFrame,
                        text = '*',
                        width = 1,
                        height = 1).grid(row=i+1,
                                        column=col + 1)
def generateGUI():
    for widget in listFrame.winfo_children():
        widget.destroy()
    dish_lists = grabMenus(Parameters)

    generateMenu(dish_lists[0], 0) #carillo
    generateMenu(dish_lists[1], 2) #dlg
    generateMenu(dish_lists[2], 4) #ortega
    generateMenu(dish_lists[3], 6) #portola

#loop
buttonBrunch = meals(topFrame,
                        text="Brunch",
                        width=12,
                        bg = "white",
                        relief="raised")
buttonBrunch.set_ID(0)
buttonBrunch.grid(row = 2, column = 0)

buttonBreakfast = meals(topFrame,
                        text="Breakfast",
                        width=12,
                        bg = "white",
                        relief="raised")
buttonBreakfast.grid(row = 2, column = 1)
buttonBreakfast.set_ID(1)

buttonLunch = meals(topFrame,
                    text="Lunch",
                    width=12,
                    bg = "white",
                    relief="raised")
buttonLunch.grid(row = 2, column = 2)
buttonLunch.set_ID(2)

buttonDinner = meals(topFrame,
                    text="Dinner",
                    width=12,
                    bg = "white",
                    relief="raised")
buttonDinner.grid(row = 2, column = 3)
buttonDinner.set_ID(3)

#date selection buttons
buttonToday = dates(topFrame,
                        text="Today",
                        width=12,
                        bg = "white",
                        relief="raised")
buttonToday.grid(row = 1, column = 0)
buttonToday.set_ID(date_string_list[0])

buttonTomorrow = dates(topFrame,
                        text="Tomorrow",
                        width=12,
                        bg = "white",
                        relief="raised")
buttonTomorrow.grid(row = 1, column = 1)
buttonTomorrow.set_ID(date_string_list[1])
for i in range(2, 7):
    buttonDates = dates(topFrame,
                            text=date_string_list[i],
                            width=12,
                            bg = "white",
                            relief="raised",)
    buttonDates.grid(row = 1, column = i)
    buttonDates.set_ID(date_string_list[i])


#apply button
buttonApply = Button(topFrame,
                        text = 'Apply',
                        width=12,
                        bg='white',
                        relief='raised',
                        command = generateGUI)
buttonApply.grid(row = 2, column = 6)



#dining common labels
labelCarrillo = Label(bottomFrame,
                 text="Carrillo",
                 width=28,
                 anchor = W).grid(row = 0,
                                column = 0)

labelDLG = Label(bottomFrame,
                 text="De La Guerra",
                 width=28,
                 anchor = W).grid(row = 0,
                                column = 1)

labelOrtega = Label(bottomFrame,
                 text="Ortega",
                 width=28,
                 anchor = W).grid(row = 0,
                                column = 2)

labelPortola = Label(bottomFrame,
                 text="Portola",
                 width=28,
                 anchor = W).grid(row = 0,
                                column = 3)

#food list labels and star buttons

grabMenus(Parameters, True)
mainloop()


