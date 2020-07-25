from django.shortcuts import render, redirect
from third.models import Restaurant,Review
from django.core.paginator import Paginator
from third.forms import RestaurantForm, ReviewForm,UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Count,Avg

def list(request):
    restaurants = Restaurant.objects.all().annotate(reviews_count=Count('review')).annotate(average_point=Avg('review__point'))
    paginator = Paginator(restaurants, 5)
    #third/list/?page= 를 이용
    page = request.GET.get('page')
    #paginator의 객체 정보가 담김 (어느 페이지인지 등등)
    items= paginator.get_page(page)

    context = {
        'restaurants' : items
    }
    return render(request,'third/list.html', context)


#POST요청으로 들어온 데이터를 자동으로 RestaurantForm에 담아서 저장할 수 있음
def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/third/list/')
    # POST가 아니면 render로 처리
    form = RestaurantForm()
    return render(request, 'third/create.html', {'form': form})


def update(request):
    #POST로 진입 되었는데, id가 실제 있는것인지 확인
    if request.method == 'POST' and 'id' in request.POST:
        #POST이면 데이터 수정 Restaurant = models
        #요청해서 들어온 해당 값을 불러옴
        item = get_object_or_404(Restaurant, pk=request.POST.get('id')) #page 없음 화면
        #데이터가 없다면 빈 string이 전달
        password = request.POST.get("password","")
        #request.POST를 이용해서 instance를 초기화,
        # RestaurantForm에 수정을 원하는 실제 변경 값을 넣어줌
        # item은 실제 데이터 값 update 하도록 해줌 -> 없으면 create됨
        #updateRestaruantForm으로 수정, Update용이기 때문에
        form = UpdateRestaurantForm(request.POST, instance=item)
        #password가 일치하면, 수정 저장
        if form.is_valid() and password == item.password :
            item = form.save()
    elif request.method == 'GET':
        #GET이면 query parameter로 data가 들어온다는 가정하에 진행
        # item = Restaurant.objects.get(pk=request.GET.get('id')) ##third/update?id=2
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        #RestaurantForm으로 GET한 아이디값으로 지정,
        form = RestaurantForm(instance=item)
        #update화면으로 보냄, create랑 동일
        return render(request,'third/update.html',{'form': form})
    #일반적인 POST는 Redirect를 통해 list화면으로 보냄
    #id 값이 없으면 list 화면으로 돌아감
    return HttpResponseRedirect('/third/list/')


def detail(request, id):
    if id is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'third/detail.html', {'item': item, 'reviews': reviews})
    return HttpResponseRedirect('/third/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    #password가 전달되었을 때
    if request.method == 'POST' and 'password' in request.POST:
        #password 비교해서 아이템 삭제
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('/third/list/') #삭제되면 list 페이지로 보냄(view.name사용)
        #만약 비밀번호가 입력되지 않았으면, 상세화면으로 다시 되돌려 보냄
        return redirect('restaurant-detail',id=id)
    #get으로 접근했을 때, 비밀번호 입력 페이지를 render를 통해서 delete 페이지로 보냄
    return render(request, 'third/delete.html', {'item':item})


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return redirect('restaurant-detail', id=restaurant_id)
    #Review 처음 form 제작하고 난 후에 위의 POST 실행이 됨
    item = get_object_or_404(Restaurant, pk=restaurant_id)
    #어떤 restaruant인지 db에서가져와 id 값을 initial의 속성으로 전달
    form = ReviewForm(initial={'restaurant' : item})
    return render(request, 'third/review_create.html',{'form': form, 'item': item}) #item = restaurant_id


def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()
    return redirect('restaurant-detail',id=restaurant_id)#Restaurant 상세화면으로 돌아감


def review_list(request):
    #최신순 정렬 -created_at
    reviews = Review.objects.all().select_related().order_by('-created_at')
    paginator = Paginator(reviews, 10)

    page = request.GET.get('page')
    #paginator해서 추려낸 정보만 출력
    items = paginator.get_page(page)

    context = {
        'reviews' : items
    }
    return render(request, 'third/review_list.html', context)