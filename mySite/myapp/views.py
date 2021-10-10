import json
from django.shortcuts import redirect, render
import requests
from requests import api
from . import mongodb
from django import forms
from django.views.decorators.csrf import csrf_exempt
#   DC96889C-7090-A445-9806-FBA2D0C8508BC622FA93-8506-41C2-9F56-8FCCC11F35DB 
#   215E7ED2-8B7D-2842-A5B0-B6F438ECB5998AB6FBC2-59BA-41CC-B54C-B96011624A9B 
#just past your own api key into the url after localhost/myapp to start building your mongodb database... it takes a while...
apikey='215E7ED2-8B7D-2842-A5B0-B6F438ECB5998AB6FBC2-59BA-41CC-B54C-B96011624A9B'
server=mongodb.get_database()

class api_keyForm(forms.Form):
    api_key = forms.CharField(label='api_key', max_length=100)

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res
def api(arg,apikey):
    #   My Own API Key you may use yours if you'd like
    url=f'https://api.guildwars2.com/v2/{arg}'
    response=requests.get(url,data={'access_token':apikey})
    print(f"Requesting Data-from-{url}->")
    if(type(response.json())==dict and response.json()['text']=='Invalid access token'):
        return render(response)
    return response.json()
def getItem(arg,apikey):
    if(arg):
        return api(f'items/{arg}',apikey)
def getItemStats(arg,apikey):
    if(arg):
        return api(f'itemstats/{arg}',apikey)
def listCharacters(arg,apikey):
    if(arg):
        return api(f'characters/{arg}',apikey)
    else:
        return api('characters/',apikey)
def listEquipment(arg,apikey):
    return listCharacters(f'{arg}',apikey)

def build(request, apikey):
    equipmentList={}
    context={}
    characterlist=existsCharacter(apikey)
    for character in characterlist:
        equipmentList[character]=(existsEquipment(character,apikey))
    context['characters']=characterlist
    context['equipments']=equipmentList
    for items in context['equipments']:
        context['equipments'][items]=context['equipments'][items][items]
        for item in context['equipments'][items]:
            try :
                upgradeList=[]
                for upgrade in item['upgrades']:
                    upgradeList.append(existsUpgrade(upgrade,apikey))
                item['upgrades']=upgradeList
            except: 
                item['upgrades']={'Non'}
            try:
                item['stats']
            except:
                item['stats']={'attributes': "Not Given"}
            newItem=existsItems(item['id'],apikey)
            item['id']=newItem['name']
            item['icon']=newItem['icon']
            try:
                attributesList={}
                for x in newItem['details']['infix_upgrade']['attributes']:
                    attributesList[x["attribute"]]=x["modifier"]
                item['stats']={'attributes':attributesList}
            except:
                ""
    return context
@csrf_exempt
def index(request):
    #my api key
    try:
        if(request.method=='POST'):
            if(len(request.POST.get("api_key", ""))>0):
                return key(request,request.POST.get("api_key", ""))
            elif(len(request.POST.get("api_key", ""))==0):
                return render(request,"chars.html",build(request,apikey))  
    except:
        return render(request,"index.html")
@csrf_exempt
def key(request,api_key):
    #your api key
    apikey=api_key
    return render(request,"chars.html",build(request,apikey))   

def putCharacters(apikey):
    responseJson=listCharacters("",apikey)
    # print("=MongoDB-Putting-into-Accounts-Context")
    accounts_collection=server['accounts']
    accounts_collection.insert_one({'_id':apikey,'characters':responseJson})
    return responseJson
def putCharacterEquipment(charName,apikey):
    responseJson=listCharacters(charName,apikey)
    # print("=MongoDB-Putting-Into-Characters-Context")
    characters_collection=server['characters']
    characters_collection.insert_one(Merge({'_id':charName},responseJson))
    return responseJson
def putItems(id,apikey):
    responseJson=getItem(id,apikey)
    # print("=MongoDB-Putting-Into-Items-Context")
    characters_collection=server['items']
    characters_collection.insert_one(Merge({'_id':id},responseJson))
    return responseJson
def exists(collection,id):
    # print(f"=MongoDB-Pulling-From-[Item: {id}]-From-[Conext: {collection}]")
    collection_item=server[collection]
    result=collection_item.find({'_id':id})
    if result.count()==0:
        return False
    else:
        return result

def existsCharacter(apikey):
    charList={}
    temp=exists('accounts',apikey)
    if temp:
        charList=temp.distinct('characters')
    else:
        charList=putCharacters(apikey)
    return charList
    
def existsEquipment(character,apikey):
    equipmentList={}
    temp=exists('characters',character)
    if temp:     
        equipmentList[character]=(temp.distinct('equipment'))
    else:
        equipmentList[character]=(putCharacterEquipment(character,apikey))['equipment']
    return equipmentList
    
def existsItems(id,apikey):
    itemList=''
    temp=exists('items',id)
    if temp:     
        itemList=temp[0]
    else:
        itemList=putItems(id,apikey)
    return itemList

def existsUpgrade(id,apikey):
    itemList=''
    temp=exists('items',id)
    if temp:     
        itemList=temp[0]['name']
    else:
        itemList=putItems(id,apikey)[0]['name']
    return itemList

