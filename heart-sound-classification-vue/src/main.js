import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';

// 导入页面组件
import NavBar from './components/NavBar.vue';
import NavBar_ from './components/NavBar_.vue';
import UserRegister from './components/UserRegister.vue';
import UserLogin from './components/UserLogin.vue';
import UploadForm from './components/UploadForm.vue';
import HistorySearch from './components/HistorySearch.vue';

Vue.config.productionTip = false;

// 告诉Vue使用Vue Router
Vue.use(VueRouter);

// 定义路由
const routes = [
  { path: '/', component: NavBar },
  { path: '/_', component: NavBar_ },
  { path: '/Register', component: UserRegister },
  { path: '/UserLogin', component: UserLogin },
  { path: '/upload', component: UploadForm },
  { path: '/history-search', component: HistorySearch }
];

// 创建路由实例
const router = new VueRouter({
  routes, // 短语法，相当于 routes: routes
  mode: 'history' // 使用HTML5 history模式
});

new Vue({
  router, // 将路由挂载到Vue根实例中
  render: h => h(App),
}).$mount('#app');