﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import subList
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf
import time



# Construccion de modelos

def newCatalog():
    catalog = {'videos': None,
               'categories': None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['categories'] = lt.newList('ARRAY_LIST', cmpfunction=comparecat)

    return catalog


# Funciones para agregar informacion al catalogo

def addvideo(catalog, video):
    lt.addLast(catalog["videos"], video)


def addcategory(catalog, cat):  
    poscat = lt.isPresent(catalog["categories"], cat["id"])

    if poscat == 0:
        c = newcategory(cat["name"].strip(), cat["id"])
        lt.addLast(catalog["categories"], c)


# Funciones para creacion de datos

def newTag(name):
    tag = {'name': "", 'videos': None}
    tag['name'] = name
    tag['videos'] = lt.newList('ARRAY_LIST')
    return tag


def newcategory(name, id):
    cat = {"id": "", "name":""}
    cat["id"] = id
    cat["name"] = name
    return cat


# Funciones de consulta

def getCategoryId(catalog, category_name):
    for n in range(1,lt.size(catalog["categories"])+1):
        category = lt.getElement(catalog["categories"], n)
        if category["name"].lower() == category_name.lower():
            return category["id"]
    return None


def getBestViews(catalog, category_id, country):
    listcopy = catalog["videos"].copy()
    sorted_list = sortVideoCountryCategory(listcopy)
    #uso de merge: nlog(n)
    posvideo = lt.binarySearch(sorted_list, country, "country")

    first = False
    while posvideo > 1 and not first:
        if lt.getElement(sorted_list, posvideo-1)['country'] == country:
            posvideo -= 1
        else:
            first = True
    #es para ubicar el primer elemento de la lista de pais en especifico, hay 10 paises -> maximo n/10 

    sub_list = lt.newList('ARRAY_LIST')
    while lt.getElement(sorted_list, posvideo)['country'] == country:
        if lt.getElement(sorted_list, posvideo)['category_id'] == category_id:
            lt.addLast(sub_list, lt.getElement(sorted_list, posvideo))
        elif not lt.isEmpty(sub_list):
            return sub_list
        posvideo += 1
    #recorre unicamente mientras no cambiemos de pais -> n/10

    return sub_list


def getTrendCategory(catalog, category_id):
    listcopy = catalog["videos"].copy()
    sorted_list = sortVideoCategoryTitle(listcopy)
    #uso de merge: O(nlog(n)) por merge (3 merge usados)
    posvideo = lt.binarySearch(sorted_list, category_id, "category_id")
    #busqueda binaria: O(log(n))
    first = False
    while posvideo > 1 and not first:
        if lt.getElement(sorted_list, posvideo-1)['category_id'] == category_id:
            posvideo -= 1
        else:
            first = True
    #en el peor de los casos recorre O(m) donde m es igual al número total de videos que hay en esa categoría

    postrend = posvideo
    trendtitle = ""
    trendcount = -1
    count = 0
    while lt.getElement(sorted_list, posvideo)['category_id'] == category_id:
        if posvideo == 1:
            trendtitle = lt.getElement(sorted_list, postrend)['title']
        elif lt.getElement(sorted_list, posvideo)['title'] != lt.getElement(sorted_list, posvideo-1)['title']:
            if count > trendcount:
                trendcount = count
                postrend = posvideo-1
                trendtitle = lt.getElement(sorted_list, postrend)['title']
            count = 1
        elif (lt.getElement(sorted_list, posvideo)['trending_date'] != lt.getElement(sorted_list, posvideo-1)['trending_date']):
            count += 1
        posvideo += 1
    #O(m)
    
    video = lt.getElement(sorted_list, postrend)
    sorted_list.clear()
    return video, trendcount


def getTrendCountry(catalog, country):
    listcopy = catalog["videos"].copy()

    sorted_list = sortVideoByCountry(listcopy)
    #uso de merge: nlog(n)
    posvideo = lt.binarySearch(sorted_list, country, "country")
    #busqueda binaria: log(n)
    first = False

    while posvideo >= 1 and not first:
        if lt.getElement(sorted_list, posvideo)["country"] == lt.getElement(sorted_list, posvideo-1)["country"]:
            posvideo -=1
        else:
            first = True
    #es para ubicar el primer elemento de la lista de pais en especifico, hay 10 paises -> maximo n/10 
    posicion = posvideo
    conteo = 1
    Last = False

    while not Last and posicion < lt.size(sorted_list):
        if lt.getElement(sorted_list, posicion)["country"] == lt.getElement(sorted_list, posicion+1)["country"]:
            conteo += 1
            posicion +=1
        else:
            Last = True
    #cuenta videos de un pais -> n/10
    CountryList = lt.subList(sorted_list, posvideo, conteo)
    #n/10
    

    SortedCountryList = sortVideoById(CountryList)
    #n/10

    histograma = {}
    i = 0
    while i < lt.size(SortedCountryList):

        Url = lt.getElement(SortedCountryList, i)["video_id"]
        histograma[Url] = histograma.get(Url, 0) +1
        i +=1
    #n/10
    
    mayor = max(histograma.values())

    for Url in histograma:
        if(histograma[Url] == mayor):
            UrlVideoTrend = Url
            break
    #n/10
    posTrendVideo = lt.binarySearch(SortedCountryList, UrlVideoTrend, "video_id")

    return lt.getElement(SortedCountryList, posTrendVideo),  mayor


def getBestTag(catalog, tagname, country):
    listcopy = catalog["videos"].copy()
    sorted_list = sortVideoByCountry(listcopy)
    #uso de merge: O(nlog(n))
    posvideo = lt.binarySearch(sorted_list, country, "country")
    #busqueda binaria: O(log(n))
    first = False
    while posvideo >= 1 and not first:
        if lt.getElement(sorted_list, posvideo)["country"] == lt.getElement(sorted_list, posvideo-1)["country"]:
            posvideo -=1
        else:
            first = True
    #en el peor de los casos recorre O(m) donde m es igual al número total de videos que hay para ese país
    
    pos = posvideo
    count = 1
    last = False

    while not last and pos < lt.size(sorted_list):
        if lt.getElement(sorted_list, pos)["country"] == lt.getElement(sorted_list, pos+1)["country"]:
            count += 1
            pos +=1
        else:
            last = True
    #O(m)
    
    CountryList = lt.subList(sorted_list, posvideo, count)

    taglist = lt.newList('ARRAY_LIST', cmpfunction=comparetags)

    for n in range(1, lt.size(CountryList)+1):
        video = lt.getElement(CountryList, n)
        videotags = video['tags'].split('"|"')
        for videotag in videotags:
            addVideoTags(taglist, videotag.strip('"'), video)
            #O(l) donde l es el numero de tags del video
    #O(m)

    tagpos = lt.isPresent(taglist, tagname)

    if tagpos > 0:
        videos = lt.getElement(taglist, tagpos)['videos']
        return sortVideoByViews(videos)
    else:
        return None


def addVideoTags(taglist, tagname, video):
    postag = lt.isPresent(taglist, tagname)
    if postag > 0:
        tag = lt.getElement(taglist, postag)
    else:
        tag = newTag(tagname)
        lt.addLast(taglist, tag)
    lt.addLast(tag['videos'], video)


# Funciones utilizadas para comparar elementos dentro de una lista

def comparetags(tag1, tag):
    if (tag1.lower() in tag['name'].lower()):
        return 0
    return -1


def organizetags(tag1, tag2):
    return (tag1["name"] < tag2["name"])


def comparecat(cat1, cat):
    if (cat1 in cat['id']):
        return 0
    return -1


def cmpVideosByViews(video1, video2):
    return (int(video1["views"]) > int(video2["views"]))


def cmpVideosByCategory(video1, video2):
    return (int(video1["category_id"]) < int(video2["category_id"]))


def cmpVideosByCountry(video1, video2):
    return (video1["country"] < video2["country"])


def cmpVideosByTitle(video1, video2):
     return (video1["title"] < video2["title"])


def cmpVideosByTrend(video1, video2):
    return (video1['trending_date'] < video2['trending_date'])

def cmpVideosById(video1, video2):
    return (video1["video_id"] < video2["video_id"])


# Funciones de ordenamiento

def sortVideoCountryCategory(videos):
    return merge.sort(merge.sort(merge.sort(videos, cmpVideosByViews), cmpVideosByCategory), cmpVideosByCountry)


def sortVideoCategoryTitle(videos):
    return merge.sort(merge.sort(merge.sort(videos, cmpVideosByTrend), cmpVideosByTitle), cmpVideosByCategory)

def sortVideoByCountry(videos):
    result = merge.sort(videos, cmpVideosByCountry)
    return result

def sortVideoById(videos):
    result = merge.sort(videos, cmpVideosById)
    return result

def sortVideoByViews(videos):
    return merge.sort(videos, cmpVideosByViews)

def sortVideoByTitle(videos):
    result = merge.sort(videos, cmpVideosByTitle)
    return result
