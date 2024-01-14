from bs4 import BeautifulSoup
import requests
from tkinter import *
from datetime import timedelta, date
import os.path

DCdict = {1: 'Carrillo', 2: 'De La Guerra', 3: 'Ortega', 4: 'Portola'}
Mealdict = {0: 'Brunch', 1: 'Breakfast', 2: 'Lunch', 3: 'Dinner'} 
today = str(date.today())
Parameters = [today, 3, 0] #for calling grabMenus, with default values
all_dishes_list = []
colorVeg = '#a3d092'
colorNoVeg = '#c7e2bd'
colorBg = 'white'
colorText = '#292929'
colorStar = '#FFFFF0'
colorToggleOff= "#c7a68f"
colorToggleOn = '#825426'
colorToggleOffDate='#B9BBB6'
colorToggleOnDate='#5B5C5E'

#widget object
window = Tk()
window.title("GauchoGrub")
window.configure(background=colorBg)

#list of starred foods
favFoods = []
#create a file if no file, and not overwriting the original
if(not os.path.isfile('favFood.txt')):
    file = open('favFood.txt', 'w+')

#this can also fix the problem
#file = open('favFood.txt', 'a+')
#file.close()
file = open('favFood.txt', 'r')
for line in file:
    favFoods.append(line[0 : len(line) - 1])
#for debugger
#print(favFoods)
#create array of 7 days
date_string_list = []

#initialize data_string_list
for i in range(7):
    day = date.today() + timedelta(days=i)
    string = str(day)
    #print(string)
    date_string_list.append(string)

#meal and date selection frame 
topFrame = Frame(window, width=100, height=3, bg = colorBg)
topFrame.grid(row = 0, column = 0)

#list of foods frame
listFrame = Frame(window, width=100, height = 3, bg = colorBg)
listFrame.grid(row = 2, column = 0)

#object for toggle button for meal selection
class meals(Button):
    registry = [] #ensuring that clicking one will unclick another 
    #similar construct in date
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
            self.config(bg = colorToggleOff)
            Parameters[1] = -1 #changes parameter for apply -> grabMenu
            #similar construct for date and veg/v buttons
        else:
            self.config(relief="sunken")
            self.config(bg = colorToggleOn)
            Parameters[1] = self.ID
            for meal in self.registry:
                if meal != self:
                    #print(meal)
                    meal.config(relief="raised")
                    meal.config(bg = colorToggleOff)
    

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
            self.config(bg = colorToggleOffDate)
            Parameters[0] = ""
        else:
            self.config(relief="sunken")
            self.config(bg = colorToggleOnDate)
            Parameters[0] = self.ID
            for date in self.registry:
                if date != self:
                    #print(date)
                    date.config(relief="raised")
                    date.config(bg = colorToggleOffDate)

#toggle button for all stars button
class star(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command = self.click_function)
    def click_function(self):
        x, y = self.grid_info()["column"], self.grid_info()["row"]
        #if clicked, this will grab the dish name on the side
        food = listFrame.grid_slaves(y, x-1)[0]['text']
        #and add or delete it from fav food
        if self.config('relief')[-1] == 'sunken':
            self.config(relief="raised")
            self.config(bg = colorStar)
            if food in favFoods:
                favFoods.remove(food)
        else:
            self.config(relief="sunken")
            self.config(bg = "gold")
            if food not in favFoods:
                favFoods.append(food)
        #for debugging
        #print(x, y)
        #print(favFoods)
class veg(Button):
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
            self.config(bg = colorNoVeg)
            Parameters[2] = 0
        else:
            self.config(relief="sunken")
            self.config(bg = colorVeg)
            Parameters[2] = self.ID
            for veg in self.registry:
                if veg != self:
                    veg.config(relief="raised")
                    veg.config(bg = colorNoVeg)

# format of the url: 
# https://apps.dining.ucsb.edu/menu/day?dc=carrillo&d=2024-01-13&m=breakfast&m=brunch&m=lunch&m=dinner&m=late-night&food=

#generate the target url for information scraping on UCSB dining menu website 
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
#grab menus based on Parameters[date, meal, veg/v or not]
def grabMenus(Para, Printable = False):
    #if no selection of date or meal
    if(Para[1] == -1 or Para[0] == ""):
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
                item = item[0 : index + 1] + item[item.find('&') + 5:]
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

#check function for online scrapping 
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

def generateMenu(menu, col):
    #generate the dining commons name label 
    labelDc = Label(listFrame,
                 text= DCdict[1 + col/2],
                 width = 37,
                 anchor = CENTER,
                 bg = colorBg,
                 fg = colorText).grid(row = 0,
                                column = col, columnspan = 2)
    if(len(menu) == 0):
        #no food from here
        food = Label(listFrame,
                        text = "Food is not available here",
                        width = 37,
                        pady = 5, 
                        bg = colorBg,
                        fg = colorText).grid(row = 1,
                                        column = col)
        #blank out the menu
        for i in range(1,26):
            food = Label(listFrame,
                            text = "",
                            width = 37,
                            pady = 5, 
                            bg = colorBg,
                            fg=colorText).grid(row = i+1,
                                            column = col)
    color = colorBg
    for i in range(len(menu)):
        #check for vegan and vegetarian 
        #vegetarian can eat vegan food, not vice versa
        if(Parameters[2] == 1):
            if(menu[i].find("(vgn)") > 0 or menu[i].find("(v)") > 0):
                color = colorVeg
        elif(Parameters[2] == 2):
            if(menu[i].find("(vgn)") > 0):
                color = colorVeg
        food = Label(listFrame,
                            text = menu[i],
                            width = 34,
                            pady = 5, 
                            bg = color,
                            fg=colorText).grid(row = i+1,
                                            column = col)
        color = colorBg
        #if already in favorite food, starred
        if menu[i] in favFoods:
            Button = star(listFrame,
                            text = '*',
                            width = 1,
                            height = 1,
                            bg = 'gold',
                            relief = 'sunken').grid(row=i+1,
                                            column=col + 1)
        else:
            Button = star(listFrame,
                            text = '*',
                            width = 1,
                            height = 1,
                            bg = colorStar).grid(row=i+1,
                                            column=col + 1)

#save and delete from document favFood.txt --> makes favorite food list lasting 
def saveFavFoods(favFoods):
    file = open("favFood.txt", 'w')
    txt = ""
    for food in favFoods:
        txt += food + "\n"
    file.write(txt)
    file.close()

#functino to generative menus
def generateGUI():
    #clear all previous menus
    for widget in listFrame.winfo_children():
        widget.destroy()
    dish_lists = grabMenus(Parameters)

    generateMenu(dish_lists[0], 0) #carillo
    generateMenu(dish_lists[1], 2) #dlg
    generateMenu(dish_lists[2], 4) #ortega
    generateMenu(dish_lists[3], 6) #portola
    saveFavFoods(favFoods) #save/delete food into .txt

#buttons for each meal 
buttonBrunch = meals(topFrame,
                        text="Brunch",
                        width=12,
                        bg = colorToggleOff,
                        relief="raised")
buttonBrunch.set_ID(0) #ID determines which one is called --> changes Parameters
buttonBrunch.grid(row = 2, column = 0)

buttonBreakfast = meals(topFrame,
                        text="Breakfast",
                        width=12,
                        bg = colorToggleOff,
                        relief="raised")
buttonBreakfast.grid(row = 2, column = 1)
buttonBreakfast.set_ID(1)

buttonLunch = meals(topFrame,
                    text="Lunch",
                    width=12,
                    bg = colorToggleOff,
                    relief="raised")
buttonLunch.grid(row = 2, column = 2)
buttonLunch.set_ID(2)

buttonDinner = meals(topFrame,
                    text="Dinner",
                    width=12,
                    bg = colorToggleOn,
                    relief="sunken")
buttonDinner.grid(row = 2, column = 3)
buttonDinner.set_ID(3)

#date selection buttons
#default date is today, thus setting is initialized differently
buttonToday = dates(topFrame,
                        text="Today",
                        width=12,
                        bg = colorToggleOnDate,
                        relief="sunken")
buttonToday.grid(row = 1, column = 0)
buttonToday.set_ID(date_string_list[0])

buttonTomorrow = dates(topFrame,
                        text="Tomorrow",
                        width=12,
                        bg = colorToggleOffDate,
                        relief="raised")
buttonTomorrow.grid(row = 1, column = 1)
buttonTomorrow.set_ID(date_string_list[1])
#for the subsequent days 
for i in range(2, 7):
    buttonDates = dates(topFrame,
                            text=date_string_list[i],
                            width=12,
                            bg = colorToggleOffDate,
                            relief="raised",)
    buttonDates.grid(row = 1, column = i)
    buttonDates.set_ID(date_string_list[i])


#apply button
buttonApply = Button(topFrame,
                        text = 'Apply',
                        fg = colorToggleOn,
                        width=12,
                        bg= 'gold',
                        relief='raised',
                        command = generateGUI)
buttonApply.grid(row = 2, column = 6)

#vegetarian and vegan button
buttonVegetarian = veg(topFrame,
                          text = 'Vegetarian',
                          width = 12,
                          bg = colorNoVeg,
                          relief='raised')
buttonVegetarian.grid(row = 2, column = 4)
buttonVegetarian.set_ID(1)
buttonVegan = veg(topFrame,
                          text = 'Vegan',
                          width = 12,
                          bg = colorNoVeg,
                          relief='raised')
buttonVegan.grid(row = 2, column = 5)
buttonVegan.set_ID(2)

mainloop()
