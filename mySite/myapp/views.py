from django.shortcuts import render
from django.http import HttpResponse, response
import requests
from requests import api
from . import mongodb
#DC96889C-7090-A445-9806-FBA2D0C8508BC622FA93-8506-41C2-9F56-8FCCC11F35DB 
#215E7ED2-8B7D-2842-A5B0-B6F438ECB5998AB6FBC2-59BA-41CC-B54C-B96011624A9B 
#just past your own api key into the url after localhost/myapp to start building your mongodb database... it takes a while...
server=mongodb.get_database()
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res
def api(arg,apikey):
    #   My Own API Key you may use yours if you'd like
    url=f'https://api.guildwars2.com/v2/{arg}'
    response=requests.get(url,data={'access_token':apikey})
    print(f"Requesting Data-from-{url}->")
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
    # print(equipmentList)
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

def index(request):
    #my api key
    apikey='215E7ED2-8B7D-2842-A5B0-B6F438ECB5998AB6FBC2-59BA-41CC-B54C-B96011624A9B'
    return render(request,"chars.html",build(request,apikey))   
def key(request,api_key):
    #your api key
    apikey=api_key
    return render(request,"chars.html",build(request,apikey))   
def putCharacters(apikey):
    responseJson=listCharacters("",apikey)
    print("=MongoDB-Putting-into-accounts")
    accounts_collection=server['accounts']
    accounts_collection.insert_one({'_id':apikey,'characters':responseJson})
    return responseJson
def putCharacterEquipment(charName,apikey):
    responseJson=listCharacters(charName,apikey)
    print("=MongoDB-Putting-into-characters")
    characters_collection=server['characters']
    characters_collection.insert_one(Merge({'_id':charName},responseJson))
    return responseJson
def putItems(id,apikey):
    responseJson=getItem(id,apikey)
    print("=MongoDB-Putting-into-items")
    characters_collection=server['items']
    characters_collection.insert_one(Merge({'_id':id},responseJson))
    return responseJson
def exists(collection,id):
    print(f"=MongoDB-Pulling-From-[item: {id}]-from-[collection: {collection}]")
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

