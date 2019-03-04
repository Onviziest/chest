const log = console.log.bind(console)

const _e = (sel) => document.querySelector(sel)

const _es = (sel) => document.querySelectorAll(sel)

const on = (element, eventName, callback, useCapture=false) => {
    element.addEventListener(eventName, callback, useCapture)
}

const async = (callback) => {
    setTimeout(function() {
        callback()
    }, 0)
}

const ensure = (condition, description) => {
    if(condition) {
        log(`✔ ${description}`)
    } else {
        throw `✘ ${description}`
    }
}

const ajax = (method, path, data, callback) => {
    let r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = (event) => {
        if (r.readyState === 4) {
            let response = JSON.stringify(r.response)
            callback(r.response)
        }
    }
    r.send(data)
}
