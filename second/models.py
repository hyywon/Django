from django.db import models

# Create your models here.
#django 모델을 상속받는 post class
class Post(models.Model):
    # modeling한 속성들
    title = models.CharField(max_length=30)
    content = models.TextField()
    #data생성될 때, 자동으로 현재시간 생성
    created_at = models.DateTimeField(auto_now_add=True)
    #마지막 수정시간
    updated_at = models.DateTimeField(auto_now=True)

    #별점 카운트 보여주기


