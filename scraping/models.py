from django.db import models

class Brand(models.Model):
    url = models.TextField(primary_key=True)
    brand = models.TextField()
    model_name = models.TextField()
    model_no = models.TextField()
    photo = models.TextField()
    product_point = models.TextField()
    price = models.FloatField()
    website = models.TextField()
    os = models.TextField()
    cpu = models.TextField()
    cpu_gen = models.TextField()
    ram = models.TextField()
    disk_capacity = models.TextField()
    screen_size = models.TextField()

    class Meta:
        db_table = 'brand'

    def __str__(self) -> str:
        return f"{self.brand.upper()} ---- {self.model_name.upper()} ---- {self.price}₺ "