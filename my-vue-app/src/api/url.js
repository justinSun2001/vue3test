import service from './axios'

//用户管理API
export function getUserNum() {
    return service({
        url: '/api/getUserNum',//Api就是proxy中的target地址
        method: "get",
    })
}

export function getUserData(pageSize, currentPage) {
    return service({
        url: '/api/getUserData',//Api就是proxy中的target地址
        method: "post",
        page_size: pageSize,
        current_page: currentPage,
    })
}

export function deleteUser(ids) {
    return service({
        method: 'post',
        url: '/api/deleteUser',//Api就是proxy中的target地址
        ids: ids,
    })
}

export function uploadUser(data) {
    return service({
        method: 'post',
        url: '/api/uploadUser',//Api就是proxy中的target地址
        data: data,
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

export function updateUser(data) {
    return service({
        method: 'post',
        url: '/api/updateUser',//Api就是proxy中的target地址
        data: data,
        headers: {
            'Content-Type': 'application/json'
        }
    })
}