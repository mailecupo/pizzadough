import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import os

############################################################
#    !IMPORTANT!   CONFIGURE SCRIPT IN THIS CELL
############################################################

#Local target for data files
path = ''

#Number of pinterest recipes to load
target = 500

# Pinterest login info
pinterest_ux = ''
pinterest_pw = ''


found = true
while found:
home = req.get('https://www.foodnetwork.com/search/pizza-dough-/p/{n}'.format(n = n)).text
soup = BeautifulSoup(home, 'html.parser')
for a in soup.find_all('a'):
    for child in a.find_all():
        if child.get('class')=='m-MediaBlock__a-HeadlineText':
            l.append(a)
            break

############################################################
#    Get ingredientlists from foodnetwork recipes
############################################################

df = pd.DataFrame()

for r in l:
    home = req.get('https:'+r).text
    soup = BeautifulSoup(home, 'html.parser')
    for i in soup.findAll("p",{"class": "o-Ingredients__a-Ingredient"}):
        df = df.append({'recipe':'https:'+r, 'ingredient':i.text.strip(), 'source':'foodnetwork'}, ignore_index = True)
        
df.to_csv(os.path.join(path,'foodnetwork.csv'))

############################################################
#    Get List of Recipes from allrecipes
############################################################

l=[]
n = 0
found = True

while found:
    found = False
    n+=1
    home = req.get('https://www.allrecipes.com/recipes/1035/bread/pizza-dough-and-crusts/?page={n}'.format(n = n)).text
    soup = BeautifulSoup(home, 'html.parser')
    for a in soup.find_all('a'):
        if a.get('class'):
            if a.get('class')[0] == 'fixed-recipe-card__title-link':
                found = True
                l.append(a.get('href'))                

############################################################
#    Get ingredientlist from allrecipes
############################################################
df = pd.DataFrame()

for r in l:
    home = req.get(r).text
    soup = BeautifulSoup(home, 'html.parser')
    for e in soup.find_all(class_ = 'ingredients-item-name'):
        df = df.append({'recipe':r, 'ingredient':e.text.strip(), 'source':'allrecipes'}, ignore_index = True)

df.to_csv(os.path.join(path,'allrecipes.csv'))

