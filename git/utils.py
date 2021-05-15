from .session import get_session
from bs4 import BeautifulSoup
import requests
import json

def get_response(url):
    response = requests.get(url)
    return json.loads(response.text)

def parseString(string):
    return ' '.join(string.split())

def getUserDetail(username):
    session = get_session()
    url = "https://github.com/"+username
    page = session.get(url)
    profile_soup = BeautifulSoup(page.content, 'html.parser')
    profile = profile_soup.find('div', class_="js-profile-editable-area d-flex flex-column d-md-block")
    timeline = profile.find('div', class_="p-note user-profile-bio mb-3 js-user-profile-bio f4").find('div')
    about=''
    if timeline:
        about = timeline.text
    profile_pic = profile_soup.find('div', class_="position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0").find('img')['src']
    name = profile_soup.find('span', class_="p-name vcard-fullname d-block overflow-hidden").text
    name = parseString(name)
    user_name = profile_soup.find('span', class_="p-nickname vcard-username d-block").text
    user_name =parseString(user_name)
    return {'name': name, 'username': user_name, 'img': profile_pic, 'about': about}

def getFollow(username):
    try:
        session = get_session()
        url = "https://github.com/"+username
        page = session.get(url)
        profile_soup = BeautifulSoup(page.content, 'html.parser')
        follows = profile_soup.find('div', class_="flex-order-1 flex-md-order-none mt-2 mt-md-0").find('div').find_all('a')
        followers = follows[0].find('span').text
        followings = follows[1].find('span').text
        stars = follows[2].find('span').text
        return {"followers": followers, "followings": followings, "stars": stars}
    except:
        return False

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
        timestamp = repo.find('relative-time').text
        forkcontent = repo.find('span', class_="f6 color-text-secondary mb-1")
        project_link = 'https://github.com'+ project['href']
        des = repo.find('div').find_all('div')[1].find('p')
        temp = {'name': parseString(project_name), 'link': project_link, 'updated': timestamp}
        langx = repo.find('span', itemprop="programmingLanguage")
        fork = False
        if forkcontent:
            fork = True
            forkedLink = "https://github.com" + forkcontent.find('a')['href']
            forked = forkcontent.text
            temp['forkdata'] = {'text': forked, 'link': forkedLink}
        temp['fork'] = fork
        if langx:
            temp['lang'] = langx.text
        if des:
            temp['des'] = parseString(des.text)
        else:
            temp['des'] = None
        data.append(temp)
    return data

def getPinnedRepo(username):
    session = get_session()
    url = "https://github.com/"+username
    profile_page = session.get(url)
    profile_soup = BeautifulSoup(profile_page.content, 'html.parser')
    reposi = profile_soup.find('div', class_="js-pinned-items-reorder-container")
    title = parseString(reposi.find('h2').text)
    repolist = reposi.find('ol').find_all('li')
    reposlist = []
    for y in repolist:
        repo = {}
        repo['name'] = y.find('span').text
        repo['link'] = "https://github.com"+y.find('a')['href']
        des = y.find_all('p')[0].text
        langx = y.find('span', itemprop="programmingLanguage")
        lang = ""
        if langx:
            lang = langx.text
        forkedFlag = False
        if "Forked" in des:
            forkedFlag = True
            forkedLink = "https://github.com" + repolist[-2].find_all('p')[0].find('a')['href']
            forked = str(des)
            des = y.find_all('p')[1].text
            repo['forkdata'] = {'text': forked, 'link': forkedLink}
        repo['lang'] = lang
        repo['des'] = parseString(des)
        repo['fork'] = forkedFlag
        reposlist.append(repo)
    return {'title': title, 'repolist': reposlist}

def get_user_email(user):
    api_url = "https://api.github.com/"
    profile_url = api_url + "users/{0}".format(user)
    response = get_response(profile_url)

    if 'message' in response:
        return False

    user_name = response['name']

    if response['email']:
        return response['email']

    users_repository_url = api_url + "users/{0}/repos?type=owner&sort=updated".format(user)
    response = get_response(users_repository_url)

    for repo in response:
        if not repo['fork']:
            repo_name = repo['full_name']
            repo_commit_url = api_url + "repos/{0}/commits".format(repo_name)
            commit_reponse = get_response(repo_commit_url)

            poss = ['committer', 'author']

            for commit in commit_reponse:
                for i in poss:
                    if commit['commit'][i]['name'] == user_name:
                        email_string = commit['commit'][i]['email']
                        if "noreply" not in email_string:
                            return email_string
    return False
