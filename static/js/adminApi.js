let apiData = {
    login: '/login',
    setting: '/setting',
    sysBind: '/sysBind',
    menber: '/menber',
    sysMain: '/sysMain',
    sysCategory: '/sysCategory'
}

let setApi = (data) => {
    let result = {}
    Object.keys(data).forEach(key => {
        result[key] = '/admin' + data[key]
    })
    return result
}

const api = setApi(apiData)
