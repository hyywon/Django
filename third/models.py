from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    # default 지정하지 않으면,기존 값들도 채워야하기 때문에,
    # None을 사용하기때문에 null=True로 정의해줘야함/ null값을 사용할 수 있도록
    password = models.CharField(max_length=20,default=None,null=True)
    #image의 url을 넣어줄것이기때문에 charfield 사용
    image = models.CharField(max_length=500,default=None,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

#many(Review) to one(Restaruant)
class Review(models.Model):
    point = models.IntegerField()
    comment = models.CharField(max_length=500)
    #review가 Restaurant와 귀속되어있음,
    #ForeignKey_Relation을 나타내기 위한 것,(외부)연결을 하기위한 식별 key
    #on_delete 연관식당이 삭제될 때, 등록된 리뷰들을 처리하는 방법에 대해서 서술
    #CASCADE : 함께 삭제하겠다는 뜻 / SET_NULL : Restaruant값이 NULL로 처리하겠다
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
