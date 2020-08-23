from django.shortcuts import render, redirect
from .models import AiClass, AiStudent

# Create your views here.


def home(request):
    class_obj_list = AiClass.objects.all()

    context = {
        'class_obj_list': class_obj_list
    }
    return render(request, 'home.html', context)


# url patterns 에 있는 변수명과 일치해야한다 !
def detail(request, class_pk):
    # class_pk에 해당하는 학생들을 가져온다 ( 그 반에 속해있는 학생 )
    student_obj_list = AiStudent.objects.filter(class_num=class_pk)

    context = {
        'class_pk': class_pk,
        'student_obj_list': student_obj_list
    }
    return render(request, 'detail.html', context)


def add(request, class_pk):
    # add 로 도착하는 요청은 두 개 다! 나눠서 처리하기 위해서 조건문을 활용한다.

    # add/ 에서 form request가 왔을 때 (두번째 POST 요청)
    if request.method == 'POST':
        # 데이터베이스에 데이터를 추가하자
        AiStudent.objects.create(
            class_num=class_pk,
            name=request.POST['name'],
            phone_num=request.POST['phone_num'],
            intro=request.POST['intro'],
        )

        return redirect('detail', class_pk)

    # detail/ 에서 add로 넘어올 때 (첫번째 GET 요청)
    context = {
        'class_pk': class_pk
    }
    return render(request, 'add.html', context)
