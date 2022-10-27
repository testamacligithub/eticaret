from django.shortcuts import render
from scraping.models import Brand
import pandas as pd
from django.db.models import Q

def getData():
    global brands, brand_db, os_type, cpu, cpu_gen, ram, screen_size, website
    brands = Brand.objects.values_list('brand', flat=True).order_by('brand').distinct()
    brand_db = Brand.objects.values()
    os_type = Brand.objects.values_list('os', flat=True).order_by('os').distinct()
    Brand.objects.filter(os="FREE DOS").update(os="FREEDOS")
    cpu = Brand.objects.values_list('cpu', flat=True).order_by('cpu').distinct()
    cpu_gen = Brand.objects.values_list('cpu_gen', flat=True).order_by('cpu_gen').distinct()
    ram = Brand.objects.values_list('ram', flat=True).distinct()
    screen_size = Brand.objects.values_list('screen_size', flat=True).distinct()
    website = Brand.objects.values_list('website', flat=True).order_by('website').distinct()

def index(request):
    getData()
    global brand_db
    if request.method == "POST":
        q  = request.POST.get('q')
        get_website  = request.POST.getlist('website')
        get_brand = request.POST.getlist('brand')
        get_os = request.POST.getlist('os')
        get_cpu = request.POST.getlist('cpu')
        get_cpu_gen = request.POST.getlist('cpu_gen')
        get_ram = request.POST.getlist('ram')
        get_screen_size = request.POST.getlist('screen_size')
        min_price = request.POST.get('min-price')
        max_price = request.POST.get('max-price')
        if get_brand == []:
            get_brand = brands
        if get_os == []:
            get_os = os_type
        if get_cpu == []:
            get_cpu = cpu
        if get_cpu_gen == []:
            get_cpu_gen = cpu_gen
        if get_ram == []:
            get_ram = ram
        if get_website == []:
            get_website = website
        if get_screen_size == []:
            get_screen_size = screen_size
        if q is not None:
            multiple_q = Q(Q(brand__icontains=q) | 
            Q(model_name__icontains=q)|
            Q(website__icontains=q)
            )
            search_box = Brand.objects.filter(multiple_q)
        else:
            multiple_q = (Q(brand__in=get_brand) &
            Q(website__in=get_website) &
            Q(os__in=get_os) &
            Q(cpu__in=get_cpu) &
            Q(cpu_gen__in=get_cpu_gen) &
            Q(ram__in=get_ram) &
            Q(screen_size__in=get_screen_size)
            )
            search_box = Brand.objects.filter(multiple_q)

    else:
        search_box = brand_db
    return render(request, 'index.html', {
        'search_box': search_box,
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })

def lowPrice(request):
    getData()
    global brand_db
    if request.method == "POST":
        q  = request.POST.get('q')
        get_website  = request.POST.getlist('website')
        get_brand = request.POST.getlist('brand')
        get_os = request.POST.getlist('os')
        get_cpu = request.POST.getlist('cpu')
        get_cpu_gen = request.POST.getlist('cpu_gen')
        get_ram = request.POST.getlist('ram')
        get_screen_size = request.POST.getlist('screen_size')
        if get_brand == []:
            get_brand = brands
        if get_os == []:
            get_os = os_type
        if get_cpu == []:
            get_cpu = cpu
        if get_cpu_gen == []:
            get_cpu_gen = cpu_gen
        if get_ram == []:
            get_ram = ram
        if get_website == []:
            get_website = website
        if get_screen_size == []:
            get_screen_size = screen_size
        if q is not None:
            multiple_q = Q(Q(brand__icontains=q) | 
            Q(model_name__icontains=q)|
            Q(website__icontains=q)
            )
            search_box = Brand.objects.filter(multiple_q).order_by('price')
        else:
            multiple_q = (Q(brand__in=get_brand) &
            Q(website__in=get_website) &
            Q(os__in=get_os) &
            Q(cpu__in=get_cpu) &
            Q(cpu_gen__in=get_cpu_gen) &
            Q(ram__in=get_ram) &
            Q(screen_size__in=get_screen_size)
            )
            search_box = Brand.objects.filter(multiple_q).order_by('price')
    else:
        brand_db = Brand.objects.values().order_by("price")
        search_box = brand_db
    return render(request, 'low_price.html', {
        'search_box': search_box,
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })

def highPrice(request):
    getData()
    global brand_db
    if request.method == "POST":
        q  = request.POST.get('q')
        get_website  = request.POST.getlist('website')
        get_brand = request.POST.getlist('brand')
        get_os = request.POST.getlist('os')
        get_cpu = request.POST.getlist('cpu')
        get_cpu_gen = request.POST.getlist('cpu_gen')
        get_ram = request.POST.getlist('ram')
        get_screen_size = request.POST.getlist('screen_size')
        if get_brand == []:
            get_brand = brands
        if get_os == []:
            get_os = os_type
        if get_cpu == []:
            get_cpu = cpu
        if get_cpu_gen == []:
            get_cpu_gen = cpu_gen
        if get_ram == []:
            get_ram = ram
        if get_website == []:
            get_website = website
        if get_screen_size == []:
            get_screen_size = screen_size
        if q is not None:
            multiple_q = Q(Q(brand__icontains=q) | 
            Q(model_name__icontains=q)|
            Q(website__icontains=q)
            )
            search_box = Brand.objects.filter(multiple_q).order_by('-price')
        else:
            multiple_q = (Q(brand__in=get_brand) &
            Q(website__in=get_website) &
            Q(os__in=get_os) &
            Q(cpu__in=get_cpu) &
            Q(cpu_gen__in=get_cpu_gen) &
            Q(ram__in=get_ram) &
            Q(screen_size__in=get_screen_size)
            )
            search_box = Brand.objects.filter(multiple_q).order_by('-price')
    else:
        brand_db = Brand.objects.values().order_by("-price")
        search_box = brand_db
    return render(request, 'high_price.html', {
        'search_box': search_box,
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })

def hplp(request):
    getData()
    global brand_db
    if request.method == "POST":
        q  = request.POST.get('q')
        get_website  = request.POST.getlist('website')
        get_brand = request.POST.getlist('brand')
        get_os = request.POST.getlist('os')
        get_cpu = request.POST.getlist('cpu')
        get_cpu_gen = request.POST.getlist('cpu_gen')
        get_ram = request.POST.getlist('ram')
        get_screen_size = request.POST.getlist('screen_size')
        if get_brand == []:
            get_brand = brands
        if get_os == []:
            get_os = os_type
        if get_cpu == []:
            get_cpu = cpu
        if get_cpu_gen == []:
            get_cpu_gen = cpu_gen
        if get_ram == []:
            get_ram = ram
        if get_website == []:
            get_website = website
        if get_screen_size == []:
            get_screen_size = screen_size
        if q is not None:
            multiple_q = Q(Q(brand__icontains=q) | 
            Q(model_name__icontains=q)|
            Q(website__icontains=q)
            )
            search_box = Brand.objects.filter(multiple_q).exclude(product_point__contains="Bilgi yok").order_by("price").order_by("-product_point")
        else:
            multiple_q = (Q(brand__in=get_brand) &
            Q(website__in=get_website) &
            Q(os__in=get_os) &
            Q(cpu__in=get_cpu) &
            Q(cpu_gen__in=get_cpu_gen) &
            Q(ram__in=get_ram) &
            Q(screen_size__in=get_screen_size)
            )
            search_box = Brand.objects.filter(multiple_q).exclude(product_point__contains="Bilgi yok").order_by("price").order_by("-product_point")
    else:
        brand_db = Brand.objects.values().exclude(product_point__contains="Bilgi yok").order_by("price").order_by("-product_point")
        search_box = brand_db
    return render(request, 'hplp.html', {
        'search_box': search_box,
        'brands': brands,
        'os_type': os_type,
        'cpu': cpu,
        'cpu_gen': cpu_gen,
        'ram' : ram,
        'screen_size': screen_size,
        'brand_db': brand_db,
        'website': website,
    })