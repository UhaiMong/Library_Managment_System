from django.db import models

# Create your models here.


class Category(models.Model):
    cat = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.cat


class BookStore(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ManyToManyField(Category)  # With category
    price = models.IntegerField()
    image = models.ImageField(
        upload_to='stores/media/uploads/', blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(
        BookStore, on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=40)
    reviewText = models.TextField()
    reviewedDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"reviewed by {self.name}"
