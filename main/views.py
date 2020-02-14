from django.shortcuts import render


def main_front(request):
   return render(request, 'main/main_front.html')