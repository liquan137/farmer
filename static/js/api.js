let apiData = {
    login: '/login',
    register: '/register',
    registerReg: '/registerReg',
    verifyEmail: '/verifyEmail',
    forget: '/forget',
    publish: '/publish',
    uploadImg: '/uploadImg',
    updatePrice: '/updatePrice',
    updatePassword: '/updatePassword',
    updatePublish: '/updatePublish',
    authReg: '/authReg'
}

let setApi = (data) => {
    let result = {}
    Object.keys(data).forEach(key => {
        result[key] = '/api' + data[key]
    })
    return result
}

const api = setApi(apiData)
