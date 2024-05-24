<template>
  <div>
    <h2>登录</h2>
    <form @submit.prevent="userlogin">
      <input v-model="id" type="text" placeholder="用户ID" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit">登录</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      id: '',
      password: ''
    };
  },
  methods: {
    async userlogin() {
      try {
        const response = await axios.post('/UserLogin', {
          id: this.id,
          password: this.password
        });
        if (response.data.code === 0) {
          alert(response.data.result);
          // 存储token等操作
          localStorage.setItem('token', response.data.token); // 存储token到localStorage
          // 跳转到其他页面
          this.$router.push('/_');
        } else {
          alert(response.data.result);
        }
      } catch (error) {
        alert("登录请求发送失败");
        console.error(error);
      }
    }
  }
};
</script>