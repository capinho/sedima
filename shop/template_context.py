from .models import Category

def getCategories(request):
    cats = Category.objects.all()   
    return {
        'cats':cats
    }

