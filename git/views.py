from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .utils import getUserDetail, getPinnedRepo, getFollow, getRepo

@cache_page(60*60)
def index(request):
    return render(request, 'index.html')

@cache_page(60*60)
def gituser(request, username):
    try:
        data=getUserDetail(username)
        data['repos'] = getPinnedRepo(username)
        follows = getFollow(username)
        if follows:
            data.update(follows)
        return render(request, 'profile.html', data)
    except:
        return render(request, 'error.html')

@cache_page(60*60)
def repos(request, username):
    page = int(request.GET.get('page', default = 1))
    page_size = int(request.GET.get('page-size', default = 6))
    data = getRepo(username)
    start = (page - 1) * page_size
    end = page * page_size
    repos = data[start:end]
    context = {
        'username': username,
        'repos': repos,
        'total_repos': len(data),
        'page_size': page_size
        }
    return render(request, 'repo.html', context)


@cache_page(60*60)
def about(request):
    return render(request, 'about.html')