let apiData = {
    login: '/login',
}

let setApi = (data) => {
    let result = {}
    Object.keys(data).forEach(key => {
        result[key] = '/admin' + data[key]
    })
    return result
}

const api = setApi(apiData)
