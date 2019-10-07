const baseUrl = "/"
const qs = Qs
// 响应时间
axios.defaults.timeout = 40000
/* 配置请求头 */
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
// 配置接口地址
axios.defaults.baseURL = baseUrl
axios.defaults.withCredentials = true;
axios.interceptors.response.use((res) => {
    // 对响应数据做些事
    if (res.data.status === '200') {
        return Promise.resolve(res)
    }
    return res
}, (error) => {
    if (error.toString().indexOf('401') > 0) {
        new $.zui.Messager('您没有此权限', {
            type: 'danger'
        }).show();
    } else if (error.toString().indexOf('400') > 0) {
        new $.zui.Messager('请求相关参数错误', {
            type: 'danger'
        }).show();
    } else if (error.toString().indexOf('408') > 0) {
        new $.zui.Messager('请求超时', {
            type: 'danger'
        }).show();
    } else if (error.toString().indexOf('404') > 0) {
        new $.zui.Messager('请检查网络情况', {
            type: 'danger'
        }).show();
    } else if (error.toString().indexOf('500') > 0) {
        new $.zui.Messager('服务器宕机了 - _ -', {
            type: 'danger'
        }).show();
    } else if (error.toString().indexOf('403') > 0) {
        new $.zui.Messager('您没有此接口的权限', {
            type: 'danger'
        }).show();
    } else {
        new $.zui.Messager('服务器宕机了 - _ -', {
            type: 'danger'
        }).show();
    }
    return Promise.reject(error)
})

// 公共POST请求
let fetch_POST = (url, params) => {
    return new Promise((resolve, reject) => {
        axios.post(url, params)
            .then(response => {
                resolve(response)
            }, err => {
                reject(err)
            })
            .catch((error) => {
                new $.zui.Messager('服务器宕机了 - _ -', {
                    type: 'danger'
                }).show();
                reject(error)
            })
    })
}

// 公共GET请求
let fetch_GET = (url, params) => {
    // params = qs.stringify(params)
    console.log(params)
    return new Promise((resolve, reject) => {
        axios.get(url, {params: params})
            .then(response => {
                resolve(response)
            }, err => {
                reject(err)
            })
            .catch((error) => {
                new $.zui.Messager('服务器宕机了 - _ -', {
                    type: 'danger'
                }).show();
                reject(error)
            })
    })
}

