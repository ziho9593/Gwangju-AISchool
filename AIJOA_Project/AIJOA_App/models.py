from django.db import models

# Create your models here.

# class menu(models.Model):
    # related_name은 AiClass의 연결된 AiStudent를 뭘로 부를지를 명시
    # on_delete=models.CASCADE는 class가 삭제될 때 반의 student도 삭제 된다.
    # menu_name =
    # menu_price =
    # menu_img =

    # participate_class = models.ForeignKey(
    #     AiClass, on_delete=models.CASCADE, related_name='student')
    # # user와 1대1 매칭
    # user = models.OneToOneField(
    #     User, on_delete=models.CASCADE, related_name='student')
    # name = models.CharField(max_length=30)
    # phone_num = models.CharField(max_length=30)
    # intro_text = models.TextField()