from .session import get_session
from bs4 import BeautifulSoup


def getUserDetail(username):
    session = get_session()
    url = "https://github.com/"+username
    page = session.get(url)
    profile_soup = BeautifulSoup(page.content, 'html.parser')
    profile = profile_soup.find('div', class_="h-card mt-md-n5")
    timeline = profile.find('div', class_="p-note user-profile-bio mb-3 js-user-profile-bio f4").find('div')
    about=''
    if timeline:
        about = timeline.text
    profile_pic = profile.find('div', class_="position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0").find('img')['src']
    name = profile.find('span', class_="p-name vcard-fullname d-block overflow-hidden").text
    user_name = profile.find('span', class_="p-nickname vcard-username d-block").text
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
        timestamp = repo.find('div', class_="f6 text-gray mt-2").text
        forkcontent = repo.find('span', class_="f6 text-gray mb-1")
        project_link = 'https://github.com'+ project['href']
        des = repo.find('div').find_all('div')[1].find('p')
        temp = {'name': project_name, 'link': project_link, 'updated': timestamp[timestamp.index("Updated"):]}
        langx = repo.find('div', class_="f6 text-gray mt-2").find('span', itemprop="programmingLanguage")
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
            temp['des'] = des.text
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
    title = reposi.find('h2').text
    repolist = reposi.find('ol').find_all('li')
    reposlist = []
    for y in repolist:
        repo = {}
        repo['name'] = y.find('span').text
        repo['link'] = "https://github.com"+y.find('a')['href']
        des = y.find_all('p')[0].text
        langx = y.find('p', class_="mb-0 f6 text-gray").find('span', itemprop="programmingLanguage")
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
        repo['des'] = des
        repo['fork'] = forkedFlag
        reposlist.append(repo)
    return {'title': title, 'repolist': reposlist}
