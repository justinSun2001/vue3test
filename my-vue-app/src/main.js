import { createApp } from 'vue'

// 引入样式
import './style.css'
// 引入ElementPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 引入路由
import { router } from './router'

// 引入App组件
import App from './App.vue'

// 使用createApp创建应用
const app = createApp(App)

// 使用ElementPlus
app.use(ElementPlus)
// 使用路由
app.use(router)
// 挂载应用
app.mount('#app')