// 导出默认的Storage类
export default class Storage{
    // 获取Storage实例
    static getInstance(){
        // 如果实例不存在，则创建一个新的实例
        if(!Storage.instance){
            Storage.instance = new Storage();
        }
        // 返回实例
        return Storage.instance;
    }

    // 根据key获取localStorage中的值
    getItem(key){
        return localStorage.getItem(key);
    }

    // 根据key和值设置localStorage中的值
    setItem(key, value){
        localStorage.setItem(key, value);
    }
}