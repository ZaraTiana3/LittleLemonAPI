from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.slug

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete = models.PROTECT)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User,  on_delete = models.CASCADE, related_name='user')
    menuitem = models.ForeignKey(MenuItem, on_delete = models.CASCADE, related_name='MenuItem')
    quantity= models.SmallIntegerField(db_index=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,  db_default=2)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_default=2) 

    def save(self, *args, **kwargs):
        # Calcul automatique du prix
        self.price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('menuitem', 'user')

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(User,  on_delete = models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete = models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    def __str__(self):
        return str(self.delivery_crew)
        

class OrderItem(models.Model):
    user = models.ForeignKey(User,  on_delete = models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete = models.CASCADE ) 
    quantity = models.SmallIntegerField(db_index=True, default=0)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'menuitem')
        
#1 - admin - 3:bi_dlvr -5 Faly_ust - 7Mi_usr