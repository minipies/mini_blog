window.addEventListener('load', function () {
    let theA = document.querySelector('.disabled a')
    theA.addEventListener('click', function (e) {
        e.preventDefault()
    })
})