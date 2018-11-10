$(function () {
    $('.cart').width(innerWidth)

    total()
    $('.confirm-wrapper').click(function () {
        var cartid = $(this).attr('cartid')
        var that = $(this)

        $.get('/changecartstatus/', {'cartid':cartid}, function (response) {
            console.log(response)
            if(response.status == 1){
                var isselect = response.isselect
                if(isselect){
                    $(that).find('span').removeClass('no').addClass('glyphicon-ok')
                }else{
                    $(that).find('span').removeClass('glyphicon-ok').addClass('no')
                }
            }
            total()
        })
    })
    
    $('.all').click(function () {
        var isselect = $(this).attr('isselect')
        isselect = (isselect=='true') ? 'false' : 'true'
        $(this).attr('isselect', isselect)

        if (isselect=='true'){
            $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
        } else {
            $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
        }
        $.get('/changecartselect/', {'isselect':isselect}, function (response) {
            console.log(response)
            if(response.status==1){
                $('.confirm-wrapper').each(function () {
                    // $(this).attr('isselect', isselect)
                    if (isselect == 'true'){
                        $(this).find('span').removeClass('no').addClass('glyphicon-ok')
                    } else {
                        $(this).find('span').removeClass('glyphicon-ok').addClass('no')
                    }
                })
            }
            total()
        })
    })

    function total() {
        $.get('/total/', function (response) {
            var sum = response.sum
            $('.bill .total b').html(sum)
        })
    }

    $('#generateorder').click(function () {
        $.get('/generateorder/', function (response) {
            console.log(response)
            if (response.status == 1){  // 跳转到订单详情
                window.open('/orderinfo/'+response.identifier +
                '/', target='_self')
            }
        })
    })
})