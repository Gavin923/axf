from django.db import models

# Create your models here.
# 基础类
class Base(models.Model):
    # 图片
    img = models.CharField(max_length=100)
    # 名称
    name = models.CharField(max_length=100)
    # 商品编号
    trackid = models.CharField(max_length=10)

    class Meta:
        abstract = True


# 轮播图
class Wheel(Base):
    class Meta:
        db_table = 'axf_wheel'

# 导航
class Nav(Base):
    class Meta:
        db_table = 'axf_nav'

# 每日必购
class Mustbuy(Base):
    class Meta:
        db_table = 'axf_mustbuy'

# 商品部分
class Shop(Base):
    class Meta:
        db_table = 'axf_shop'


# 商品主体内容
class MainShow(models.Model):
    trackid = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=8)
    brandname = models.CharField(max_length=50)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=8)
    productid1 = models.CharField(max_length=8)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField()
    marketprice1 = models.FloatField()

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=8)
    productid2 = models.CharField(max_length=8)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField()
    marketprice2 = models.FloatField()

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=8)
    productid3 = models.CharField(max_length=8)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField()
    marketprice3 = models.FloatField()

    class Meta:
        db_table = 'axf_mainshow'

# 商品分类
class Foodtypes(models.Model):
    typeid = models.CharField(max_length=8) # 分类ID
    typename = models.CharField(max_length=100) # 分类名称
    childtypenames = models.CharField(max_length=256)   # 子类名称
    typesort = models.IntegerField()    # 显示先后顺序
    class Meta:
        db_table = 'axf_foodtypes'

# 商品信息
class Goods(models.Model):
    productid = models.CharField(max_length=10) # 商品ID
    productimg = models.CharField(max_length=100)   # 商品图片
    productname = models.CharField(max_length=100)  # 商品名称
    productlongname = models.CharField(max_length=100)  # 商品弄名称
    isxf = models.BooleanField(default=False)    # 精选
    pmdesc = models.BooleanField(default=False)  # 买一送一
    specifics = models.CharField(max_length=100)   # 规格
    price = models.DecimalField(max_digits=7, decimal_places=2)    # 价格
    marketprice = models.DecimalField(max_digits=7, decimal_places=2)  # 商场价格
    categoryid= models.IntegerField()   # 分类ID
    childcid = models.IntegerField()    # 子类ID
    childcidname = models.CharField(max_length=100) # 分类名称
    dealerid = models.CharField(max_length=10)  # 详情ID
    storenums = models.IntegerField()   # 库存
    productnum = models.IntegerField()  # 销量

    class Meta:
        db_table = 'axf_goods'

class User(models.Model):
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=20,unique=True)
    addr = models.CharField(max_length=256)
    img = models.CharField(max_length=100)
    rank = models.IntegerField(default=1)
    token = models.CharField(max_length=256)

    class Meta:
        db_table = 'axf_user'

# 购物车
class Cart(models.Model):
    user = models.ForeignKey(User)
    goods = models.ForeignKey(Goods)
    number = models.IntegerField()
    isselect = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'

class Order(models.Model):
    # 用户
    user = models.ForeignKey(User)
    # 创建时间
    createtime = models.DateTimeField(auto_now_add=True)
    # 状态
    # -1 过期
    # 1 未付款
    # 2 已付款，未发货
    # 3 已发货，快递
    # 4 已签收，未评价
    # 5 已评价
    # 6 退款....
    status = models.IntegerField(default=1)
    # 订单号
    identifier = models.CharField(max_length=256)

    class Meta:
        db_table = 'axf_order'

# 订单商品
class OrderGoods(models.Model):
    order = models.ForeignKey(Order)
    goods = models.ForeignKey(Goods)
    number = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_ordergoods'