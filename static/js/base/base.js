window.addEventListener('load', function () {
    function newbility(context) {
        if (context) {
            let url = 'https://cn.bing.com/search?q='+encodeURIComponent(context)
            console.log(url)
            open(url, '_blank')
        }
        console.log('什么?不行吗')
    }

    let btn = document.querySelector('#search');
    let ipt = document.querySelector('input[type="search"]');
    btn.addEventListener('click', function () {
        newbility(ipt.value.trim());
        ipt.value = ''
    })

    ipt.addEventListener('keypress', function (e) {
        if(e.key === 'Enter') {
            e.preventDefault()
            newbility(this.value.trim())
            this.value = ''
        }
    })
})
