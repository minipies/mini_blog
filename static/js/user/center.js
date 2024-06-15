
$(function () {
    // 手机号验证

    // tab栏切换
    let middles = $('.middle')
    middles.hide()
    middles.eq(1).show()
    $('.top-head li').each(function (index) {
        $(this).click(function () {
            middles.hide()
            middles.eq(index).show()
        })
    });
//     <!--发表文章-->



//     图片删除
    $('.btn-del').click(function () {
        let ok = confirm('确定删除吗？')
        if (ok) {
            let pid = $(this).attr('data-tt')
            location.href = '/article/photo_del?pid=' + pid;
        }
    })
    //
    let ph = $('#Photo')
    $('.btn-upload').click(function (e) {
        if (ph[0].files.length === 0) {
            e.preventDefault()
            console.log(ph[0])
            console.log(ph[0].files)
            console.log(ph[0].files.length)
            alert('还没有上传图片哦')
        }
    })

})