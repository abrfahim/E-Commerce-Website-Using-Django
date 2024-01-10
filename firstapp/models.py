from django.db import models

# ckeditor
from ckeditor.fields import RichTextField

#slug
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.

class Slider(models.Model):
    
    DISCOUNT_DEAL = (
        ('HOT DEALS','HOT DEALS'),
        ('New Arraivels','New Arraivels'),
    )
    
    
    Image = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=100)
    Sale = models.IntegerField()
    Brand_Name = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)
    
    def __str__(self):
        return self.Brand_Name
    

class Banner_Area(models.Model):
    Image = models.ImageField(upload_to='media/banner_img')
    Discount_Deal = models.CharField(max_length=100)
    Quote = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.Quote


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name + "--" + self.main_category.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category.main_category.name + "--" + self.category.name + '--' + self.name
    
class Section(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Color(models.Model):
    code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.code


    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    total_quantity = models.IntegerField()
    availablity = models.IntegerField()
    featured_image = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    delivery_cost = models.IntegerField(null=True)
    Product_information = RichTextField(null = True)
    model_name = models.CharField(max_length=100)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null = True)
    tags = models.CharField(max_length=100)
    description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default= '',max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.product_name
       
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)


class CouponCode(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()
    
    def __str__(self):
        return self.code
        

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)


class AdditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    

    

    