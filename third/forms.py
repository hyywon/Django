from django.forms import ModelForm
from django import forms
from third.models import Restaurant,Review
from django.utils.translation import gettext_lazy as _

REVIEW_POINT_CHOICES = {
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5)
}


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['point', 'comment', 'restaurant']
        labels = {
            'point': _('평점'),
            'comment': _('코멘트'),
        }
        help_texts = {
            'point': _('평점을 입력해주세요'),
            'comment': _('코멘트를 입력해주세요'),
        }
        #현재 어떤 레스토랑에 리뷰를 남기는지 사용자는 보여지지 않아야함
        #hidden으로 전달

        #field속성을 직접 선택해서 rendering 가능
        widgets = {
            'restaurant': forms.HiddenInput(),
            'point': forms.Select(choices=REVIEW_POINT_CHOICES)
        }

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address','image', 'password']
        labels = {
            'name': _('이름'),
            'address': _('주소'),
            'image' :_('이미지 url'),
            'password' :_('비밀번호')
        }
        help_texts = {
            'name': _('이름을 입력해주세요'),
            'address': _('주소를 입력해주세요'),
            'image' :_('이미지 url을 입력해주세요'),
            'password' :_('비밀번호를 입력해주세요')
        }
        widgets = {
            #입력하는 값이 바로 보이지 않도록하기 위해서 PasswordInput() 사용
            'password': forms.PasswordInput()
        }
        error_messages = {
            'name': {
                'max_length': _('이름을 30자 이내로 적어주세요')
            },
            'image' :{
                'max_length' :_('이미지 url을 500자 이내로 지정해주세요')
            },
            'password' :{
                'max_length' :_('비밀번호는 20자 이내로 정해주세요')
            },
        }

#수정하고자 했을 때,비밀번호를 새로 입력받는 것이 아니라 기존 비밀번호와 일치하는지 검사만 하도록
# RestaurantForm 상속
class UpdateRestaurantForm(RestaurantForm):
    class Meta:
        model = Restaurant
        #password만 제외, update하지 않겠다
        exclude = ['password']


