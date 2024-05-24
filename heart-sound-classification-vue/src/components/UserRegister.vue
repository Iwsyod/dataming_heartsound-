<template>
  <div>
    <h2>注册</h2>
    <form @submit.prevent="userregister">
      <input v-model="id" type="text" placeholder="用户ID" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <input v-model="name" type="text" placeholder="姓名" required />
      <input v-model="age" type="number" placeholder="年龄" required />
      <select v-model="gender">
        <option disabled value="">请选择性别</option>
        <option value=0>男</option>
        <option value=1>女</option>
      </select>
      <select v-model="history" required>
        <option disabled value=null>请选择病史</option>
        <option value=0>无病史</option>
        <option value=1>心脏血管疾病</option>
        <option value=2>心脏瓣膜疾病</option>
        <option value=3>心包疾病</option>
        <option value=4>心脏炎症</option>
        <option value=5>其他</option>
      </select>
      <button type="submit">注册</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      id: '',
      password: '',
      name: '',
      age: null,
      gender: null,
      history: null
    };
  },
  methods: {
    async userregister() {
      try {
        const response = await axios.post('/UserRegister', {
          id: this.id,
          password: this.password,
          name: this.name,
          age: this.age,
          gender: this.gender,
          history: this.history
        });

        // 处理注册结果
        if (response.data.code === 0) {
          alert("注册成功，请前去登录");
          // 注册成功后重定向到登录页面
          this.$router.push('/UserLogin');
        } else if (response.data.code === 2) {
          alert("该用户ID已注册，请直接登录或更换用户ID");
        } else if (response.data.code === 3) {
          alert("密码长度少于6位，注册失败");
        } else {
          alert("注册失败");
        }
      } catch (error) {
        alert("注册请求发送失败");
        console.error(error);
      }
    }
  }
};
</script>