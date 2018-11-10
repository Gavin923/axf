import hashlib
import os
import random
import time
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart, Order, OrderGoods
from myaxf import settings

# 主页
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

# 商品超市页面
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

    # 购物车数量
    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.filter(token=token)
        carts = Cart.objects.filter(user=user)
    data = {
        'foodtypes': foodtypes,
        'categoryid': categoryid,
        'childTypeList': childTypeList,
        'goodsList': goodsList,
        'childid': childid,
        'carts': carts,
    }

    return render(request, 'market/market.html', context=data)

def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg':'添加购物车成功',
        'status': 1 # 1标识添加成功，0标识添加失败，-1标识未登录
    }

    if token:   # 登录 [直接操作模型]
        # 获取用户
        user = User.objects.get(token=token)
        # 获取商品
        goods = Goods.objects.get(pk=goodsid)


        # 商品已经在购物车，只修改商品个数
        # 商品不存在购物车，新建对象（加入一条新的数据）
        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():  # 修改数量
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number'] = cart.number
        else:   # 添加一条新记录
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['number'] = cart.number

        return JsonResponse(responseData)
    else:   # 未登录 [跳转到登录页面]
        # 由于addcart这个是 用于 ajax操作， 所以这里是不能进行重定向!!
        # return redirect('axf:login')
        responseData['msg'] = '未登录，请登录后操作'
        responseData['status'] = -1
        return JsonResponse(responseData)
def subcart(request):
    # 获取数据
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')

    # 对应用户 和 商品
    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)

    # 删减操作
    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {
        'msg': '购物车减操作成功',
        'status': 1,
        'number': cart.number
    }

    return JsonResponse(responseData)
# 购物车页面
def cart(request):
    token = request.session.get('token')
    if token:  # 显示该用户下 购物车信息
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

        return render(request, 'cart/cart.html', context={'carts': carts})
    else:  # 跳转到登录页面
        return redirect('axf:login')



# 用户页面与登录，注册
def mine(request):
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        data = {
            'name': user.name,
            'rank': user.rank,
            'img': 'upload/'+user.img
        }
    else:
        data = {
            'name': '未登录',
            'img': 'upload/mine.png'
        }
    return render(request, 'mine/mine.html', context=data)

def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()

def registe(request):
    if request.method == 'GET':
        return render(request, 'mine/registe.html')
    elif request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = genarate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.addr = request.POST.get('addr')

        # 头像
        imgName = user.account + '.png'
        imagePath = os.path.join(settings.MEDIA_ROOT, imgName)
        file = request.FILES.get('icon')
        with open(imagePath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

        user.save()

        # 状态保持
        request.session['token'] = user.token

        # 重定向
        return redirect('axf:mine')
    

def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        print(password)
        print(genarate_password(password))
        try:
            user = User.objects.get(account=account)
            if user.password == genarate_password(password):
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:  # 登录失败
                return render(request, 'mine/login.html', context={'passwdErr': '密码错误!'})
        except:
            return render(request, 'mine/login.html', context={'acountErr': '账号不存在!'})


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def checkaccount(request):
    account = request.GET.get('account')
    users = User.objects.filter(account=account)
    if users.exists():
        data = {
            'msg': '账号被占用',
            'status': -1,
        }
    else:
        data = {
            'msg': '该账号可以使用',
            'status': 1,
        }
    return JsonResponse(data)

# 改变单个购物车选中状态
def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()
    data = {
        'msg': '选中状态改变',
        'status': 1,
        'isselect': cart.isselect,
    }
    print(cartid)
    return JsonResponse(data)


def changecartselect(request):
    isselect = request.GET.get('isselect')
    if isselect == 'true':
        isselect = True
    else:
        isselect = False

    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isselect
        cart.save()

    return JsonResponse({'msg': '反选操作成功', 'status': 1})


class Math(object):
    pass


def total(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user).filter(isselect=True)
    sum = 0
    for cart in carts:
        sum += cart.goods.marketprice*cart.number
    return JsonResponse({'sum':round(sum, 2), 'status':1})


def generateorder(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)
    # 订单
    order = Order()
    order.user = user
    order.identifier = str(int(time.time())) + str(random.randrange(1000,10000))
    order.save()
    #添加订单商品
    carts = Cart.objects.filter(user=user).filter(isselect=True)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = cart.goods
        orderGoods.number = cart.number
        orderGoods.save()
        #删除购物车
        cart.delete()
    data = {
        'msg':'订单生成成功',
        'status':1,
        'identifier':order.identifier,
    }
    return JsonResponse(data)


def orderinfo(request, identifier):
    # 一个订单 对应 多个商品
    order = Order.objects.get(identifier=identifier)

    return render(request, 'order/orderinfo.html', context={'order': order})


def notifyurl(request):
    return None


def returnurl(request):
    return None


def pay(request):
    return None