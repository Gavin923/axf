from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods


def home(request):
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()

    shopList = Shop.objects.all()
    shophead = shopList[0]
    shoptab = shopList[1:3]
    shopclass = shopList[3:7]
    shopcommend = shopList[7:12]

    mainshows = MainShow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows': mainshows,
    }
    return render(request, 'home/home.html', context=data)

def market(request, childid, sortid):
    # 分类信息
    foodtypes = Foodtypes.objects.all()

    # 点击的分类下标
    typeIdex = int(request.COOKIES.get('typeIndex', 0))
    # 点击分类id
    categoryid = foodtypes[typeIdex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames
    childTypeList = []
    for item in childtypenames.split('#'):
        child = {
            'childname': item.split(':')[0],
            'childid': item.split(':')[1]
        }
        childTypeList.append(child)
    print(childTypeList[0]['childname'])
    # 需要展示的商品
    if int(childid) == 0:
        goodsList = Goods.objects.all().filter(categoryid=categoryid)
    else:
        goodsList = Goods.objects.all().filter(categoryid=categoryid).filter(childcid=int(childid))

        # 排序
    if sortid == '1':  # 销量排序
        goodsList = goodsList.order_by('-productnum')
    elif sortid == '2':  # 价格最低
        goodsList = goodsList.order_by('price')
    elif sortid == '3':  # 价格最高
        goodsList = goodsList.order_by(('-price'))
    data = {
        'foodtypes': foodtypes,
        'categoryid': categoryid,
        'childTypeList': childTypeList,
        'goodsList': goodsList,
        'childid': childid,
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    return render(request, 'cart/cart.html')


def mine(request):
    return render(request, 'mine/mine.html')