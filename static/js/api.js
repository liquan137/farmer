let apiData = {
    login: '/login',
    register: '/register',
    registerReg: '/registerReg',
    verifyEmail: '/verifyEmail',
    forget: '/forget'
}

let setApi = (data) => {
    let result = {}
    Object.keys(data).forEach(key => {
        result[key] = 'api' + data[key]
    })
    return result
}

const api = setApi(apiData)
