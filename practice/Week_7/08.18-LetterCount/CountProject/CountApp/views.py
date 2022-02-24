from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def result(request):
    input_text = request.POST['input_text']

    blank_text = len(input_text)
    without_blank = len(input_text.replace(
        ' ', ''))

    return render(request, 'result.html', {'blank_text': blank_text, 'without_blank': without_blank})
