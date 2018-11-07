$(function () {
    $('.register').width(innerWidth)

    var accountOK=passwordOK=false
    $('#account input').blur(function () {
        var reg = /^[A-Za-z0-9]+$/
        if(reg.test($(this).val())){
            $('#account i').html('')
            $('#account').removeClass('has-error').addClass('has-success')
            $('#account .glyphicon').removeClass('glyphicon-remove').addClass('glyphicon-ok')
            accountOK = true
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
            passwordOK = true
        }else{
            $('#password i').html('密码由6~12位数字组成')
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password .glyphicon').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })


})