from django.shortcuts import render, redirect
from .models import Kruzok, Veduci


def import_veduci(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith("meno"):
                continue

            meno, email = line.split(',')

            Veduci.objects.get_or_create(
                email=email.strip(),
                defaults={"meno": meno.strip()}
            )


def import_kruzky(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("nazov"):
                continue

            nazov, den, miestnost, email = line.split(',')

            try:
                veduci = Veduci.objects.get(email=email.strip())
            except Veduci.DoesNotExist:
                continue

            Kruzok.objects.get_or_create(
                nazov=nazov.strip(),
                defaults={
                    "den": den.strip(),
                    "miestnost": miestnost.strip(),
                    "veduci": veduci
                }
            )


def index(request):
    if request.method == "GET":
        

        import_veduci("veduci.txt")
        import_kruzky("kruzky.txt")

        kruzky = Kruzok.objects.all()
        veduci = Veduci.objects.all()
        
        return render(request, "myApp/index.html", {
            "kruzky": kruzky,
            "veduci": veduci
        })

    
def formular(request):
    vysledok = ""

    if request.method == "POST":
        nazov = request.POST.get("nazov")
        den = request.POST.get("den")
        miestnost = request.POST.get("miestnost")
        meno = request.POST.get("veduci")
        email = request.POST.get("email")

        if not (nazov and den and miestnost and meno and email):
            vysledok = "Vyplň všetky polia!"
        else:
            veduci_obj, created = Veduci.objects.get_or_create(
                email=email.strip(),
                defaults={"meno": meno.strip()}
            )

            Kruzok.objects.create(
                nazov=nazov.strip(),
                den=den.strip(),
                miestnost=miestnost.strip(),
                veduci=veduci_obj
            )

            # 🔥 toto je kľúčové
            return redirect("formular")

    return render(request, "myApp/formular.html", {"vysledok": vysledok})