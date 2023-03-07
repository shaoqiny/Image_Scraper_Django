from django.db import models
from django.conf import settings

# Create your models here.
class Search(models.Model):
    url = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class Image(models.Model):
    search =models.ForeignKey(Search, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='search_images/')
    
    '''
    def save_image_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            file_content = ContentFile(response.content)
            self.image.save(file_content, save=True)
            '''