import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from search.models import Search, Image
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, reverse
from urllib.parse import urljoin,urlparse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def is_valid_url(url):
    # test if input is a valid url
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_image_list(url):
    # Retrive all img src in a given url and return it as a list
    img_list = BeautifulSoup(requests.get(url).content, "html.parser").find_all("img")
    img_result = []
    for img in img_list:
            img_src = img.get("src")
            if img_src:
                # If url is relative, convert it to absolute url
                image_url = urljoin(url, img_src)
                if is_valid_url(image_url):
                    # append valid image url only
                    img_result.append(image_url)
    return img_result



class SearchListView(ListView):
    model = Search
    template_name = "search/search_list.html"

    def get(self, request):
        if request.user.is_authenticated:
            # Return full search list to superuser, return private search list to user
            # This is ugly, it should be optimized
            search_list = Search.objects.all().order_by('-created_at')
            search_list_private = Search.objects.filter(owner=request.user).order_by('-created_at')

            ctx = {'search_list' : search_list, 'search_list_private': search_list_private}
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name)

    def post(self, request) :
        url = request.POST['url']
        search = Search(url=url, owner=request.user)
        search.save()
        img_list = get_image_list(url)
        for image_src in img_list:
            image_content = requests.get(image_src).content
            image = Image(search=search)
            image.image.save(image_src.split('/')[-1], ContentFile(image_content))


        return redirect(reverse('search:all'))

class SearchDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Search
    template_name = "search/search_detail.html"
    
    def get(self, request, pk) :
        """
        # render images from native image url list with get method
        url = Search.objects.get(id=pk).url
        img_list = BeautifulSoup(requests.get(url).content, "html.parser").find_all("img")
        img_result = []
        for img in img_list:
            img_src = img.get("src")
            if img_src:
                # If url is relative, convert it to absolute url
                image_url = urljoin(url, img_src)
                if is_valid_url(image_url):
                    # append valid image url only
                    img_result.append(image_url)

        context = {'img_result' : img_result}
        """
        x = Search.objects.get(id=pk)
        images = Image.objects.filter(search=x)
        context = {'img_list': images}
        return render(request, self.template_name, context)
    
    def test_func(self):
        # only super user and search.owner should see the search result
        search = self.get_object()
        return self.request.user == search.owner or self.request.user.is_superuser
