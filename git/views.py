from django.shortcuts import render
from .session import get_session
from bs4 import BeautifulSoup
from django.views.decorators.cache import cache_page

def getUserDetail(username):
    session = get_session()
    url = "https://github.com/"+username
    page = session.get(url)
    profile_soup = BeautifulSoup(page.content, 'html.parser')
    profile = profile_soup.find('div', class_="h-card mt-md-n5")
    profile_pic = profile.find('div', class_="position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0").find('img')['src']
    name = profile.find('span', class_="p-name vcard-fullname d-block overflow-hidden").text
    user_name = profile.find('span', class_="p-nickname vcard-username d-block").text
    data = [name, user_name, profile_pic]
    return data

def getFollow(username):
    session = get_session()
    url = "https://github.com/"+username
    page = session.get(url)
    profile_soup = BeautifulSoup(page.content, 'html.parser')
    follows = profile_soup.find('div', class_="flex-order-1 flex-md-order-none mt-2 mt-md-0").find('div').find_all('a')
    followers = x[0].find('span').text
    followings = x[1].find('span').text
    stars = x[2].find('span').text
    return {"followers": followers, "followings": followings, "stars": stars}

def getRepo(username):
    session = get_session()
    url = "https://github.com/"+username+"?tab=repositories"
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    repos = soup.find(id="user-repositories-list").find('ul').find_all('li')
    data = []
    for repo in repos:
        project = repo.find('div').find('div').find('h3').find('a')
        project_name = project.text
        project_link = 'https://github.com'+ project['href']
        des = repo.find('div').find_all('div')[1].find('p')
        temp = {'projectname': project_name, 'link': project_link}
        if des:
            temp['description'] = des.text
        else:
            temp['description'] = None
        data.append(temp)

    return data


def index(request):
    return render(request, 'index.html')


def gituser(request, username):
    userdetail = getUserDetail(username)
    repos = getRepo(username)
    follows = getFollow(username)
    data = {'name': userdetail[0], 'username': userdetail[1], 'img': userdetail[2], 'repos': repos}
    data.update(follows)
    return render(request, 'profile.html', data)

# def gituser(request, username):
#     try:
#         userdetail = getUserDetail(username)
#         repos = getRepo(username)
#         data = {'name': userdetail[0], 'username': userdetail[1], 'img': userdetail[2], 'repos': repos}
#         return render(request, 'profile.html', data)
#     except:
#         return render(request, 'error.html')