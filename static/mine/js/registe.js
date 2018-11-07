$(function () {
    $('.register').width(innerWidth)

    $('#account input').blur(function () {
        if($(this).val() == '') return

        var reg = /^[A-Za-z0-9]+$/
        if(reg.test($(this).val())){
            $.get('/checkaccount/', {'account':$(this).val()}, function (response) {
                console.log(response)
                if(response.status == 1){
                    $('#account i').html('')
                    $('#account').removeClass('has-error').addClass('has-success')
                    $('#account .glyphicon').removeClass('glyphicon-remove').addClass('glyphicon-ok')
                } else {
                    $('#account i').html('账号已被占用')
                    $('#account').removeClass('has-success').addClass('has-error')
                    $('#account .glyphicon').removeClass('glyphicon-ok').addClass('glyphicon-remove')
                }
            })
        }else{
            $('#account i').html('账号由数字、字母组成')
            $('#account').removeClass('has-success').addClass('has-error')
            $('#account .glyphicon').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })

    $('#password input').blur(function () {
        if($(this).val() == '') return

        var reg = /^[\d]{6,12}$/
        if(reg.test($(this).val())){
            $('#password i').html('')
            $('#password').removeClass('has-error').addClass('has-success')
            $('#password .glyphicon').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }else{
            $('#password i').html('密码由6~12位数字组成')
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password .glyphicon').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })

    $('#passwd input').blur(function () {
        if($(this).val() == $('#password input').val()){
            $('#passwd i').html('')
            $('#passwd').removeClass('has-error').addClass('has-success')
            $('#passwd .glyphicon').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }else{
            $('#passwd i').html('两次密码不一致')
            $('#passwd').removeClass('has-success').addClass('has-error')
            $('#passwd .glyphicon').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })

    $('#name input').blur(function () {
        if($(this).val() == '') return

        $('#name').removeClass('has-error').addClass('has-success')
        $('#name .glyphicon').removeClass('glyphicon-remove').addClass('glyphicon-ok')
    })

    $('#phone input').blur(function () {
        if($(this).val() == '') return

        // 手机
        var reg = /^1[3|5|7|8|]\d{9}$/
        if (reg.test($(this).val())) {
            $('#phone i').html('')
            $('#phone').removeClass('has-error').addClass('has-success')
            $('#phone .glyphicon').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        } else {    // 不符合
            $('#phone i').html('请输入正确的手机号')
            $('#phone').removeClass('has-success').addClass('has-error')
            $('#phone .glyphicon').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })
})