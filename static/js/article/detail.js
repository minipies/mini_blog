window.addEventListener('load', function () {
    let ttaa = document.querySelector('.comment-box textarea')
    let kong = true;
    ttaa.addEventListener('focus', function () {
        if (kong) {
            this.value = '';
            kong = false;
        }
    })
    let btn = document.querySelector('.btn-cmt')
    let charCountEle = document.querySelector('#Chars')
    let maxLen = ttaa.getAttribute('maxlength')
    ttaa.addEventListener('input', function (e) {
        let currentLen = ttaa.value.trim().length;
        charCountEle.textContent = maxLen - currentLen;
    });
    let form = document.querySelector('.form-comment form')
    form.addEventListener('submit', function (e) {
        let text = ttaa.value.trim();
        if (text !== '' && text !== '写下你想说的，开始我们的对话') {
            btn.disabled = true;
        } else {
            btn.disabled = false;
            btn.style.cursor = 'not-allowed';
            e.preventDefault()
        }
    });
    let lis = document.querySelectorAll('.pager li')
    lis.forEach(function (ele) {
        if (ele.classList.contains('disabled')) {
            ele.disabled = true;
            ele.style.cursor = 'not-allowed';
        } else {
            ele.disabled = false;
            ele.style.cursor = 'pointer';
        }
    })
})