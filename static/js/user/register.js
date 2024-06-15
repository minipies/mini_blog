window.addEventListener('load', function () {
    let submit = document.querySelector('button[type="submit"]')
    submit.addEventListener('click', function (e) {
        let form = document.querySelector('.form form')
        let formData = serialize(form, {hash: true, empty: true})
        if (formData.username < 2) {
            alert('用户名在2~10字之间')
            e.preventDefault()
        }
        if (formData.password < 2) {
            alert('密码应该在2~16位数')
            e.preventDefault()
        }
        if (formData.password !== formData.pwd) {
            alert('两次密码不一致')
            e.preventDefault()
        }
    })
})