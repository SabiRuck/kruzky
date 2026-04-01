from django.db import models

class Veduci(models.Model):
    meno = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.meno}"

class Kruzok(models.Model):
    nazov = models.CharField(max_length=100)
    den = models.CharField(max_length=50)
    miestnost = models.CharField(max_length=10)
    veduci = models.ForeignKey(Veduci, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nazov}"
    