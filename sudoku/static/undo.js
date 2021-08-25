async function undo(){
    if (window.square){
        window.square.querySelector('text').textContent = ''
        window.square.querySelector('circle').classList.remove('filled')
        window.square.querySelector('circle').classList.remove('wrong')
        window.square.querySelector('circle').classList.remove('matching')
        window.square.querySelector('circle').classList.add('empty')
    }
    // console.log(window.square)
}