$(function () {
    $('.market').width(innerWidth)

    //获取点击的typeIndex


    $('.type-item').click(function () {
        // $(this).addClass('active').siblings().removeClass('active')
        $.cookie('typeIndex', $(this).index(), {expires:3, path:'/'})
    })
    var typeIndex = $.cookie('typeIndex')
    if (typeIndex){ // 已经有点击分类
        $('.type-slider .type-item').eq(typeIndex).addClass('active')
    } else {    // 没有点击分类
        // 没有点击默认第一个
        $('.type-slider .type-item:first').addClass('active')
    }


    //分类按钮
    var categoreBt = false
    $('#categoryBt').click(function () {
        categoreBt = !categoreBt
        categoreBt ? categoryViewShow() : categoryViewHide()
    })
    //排序按钮
    var sortBt = false
    $('#sortBt').click(function () {
        sortBt = !sortBt
        sortBt ? sortViewShow():sortViewHide()
    })
     // 灰色蒙层
    $('.bounce-view').click(function () {
        sortBt = false
        sortViewHide()
        categoryBt = false
        categoryViewHide()
    })

    function categoryViewShow() {
        sortBt = false
        sortViewHide()
        $('.category-view').show()
        $('#categoryBt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
    }
    function categoryViewHide() {
        $('.category-view').hide()
        $('#categoryBt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')
    }
    function sortViewShow() {
        categoreBt = false
        categoryViewHide()
        $('.sort-view').show()
        $('#sortBt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
    }
    function sortViewHide() {
        $('.sort-view').hide()
        $('#sortBt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')
    }
})