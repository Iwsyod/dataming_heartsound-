<template>
  <div>
    <h2>搜索历史记录</h2>
    <input v-model="userId" type="text" placeholder="输入用户ID">
    <button @click="searchHistory">搜索</button>
    <div v-if="searching">正在搜索...</div>
    <div v-if="searchResult">
      <h3>搜索结果：</h3>
      <ul>
        <li v-for="(item, index) in searchResult" :key="index">{{ item }}</li>
      </ul>
    </div>
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
  <nav>
    <router-link to="/_">返回上级</router-link>
    <router-link to="/">退出登录</router-link>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HistorySearch',
  data() {
    return {
      userId: '',
      searchResult: null,
      searching: false,
      errorMessage: ''
    };
  },
  methods: {
    async searchHistory() {
      this.searching = true;
      this.errorMessage = '';
      this.searchResult = null;
      try {
        const response = await axios.post('/HistorySearch', {
          id: this.userId
        });
        if (response.data.code === 0) {
          this.searchResult = response.data.history_result;
        } else {
          this.errorMessage = response.data.result;
        }
      } catch (error) {
        console.error('搜索请求发送失败', error);
        this.errorMessage = '搜索请求发送失败';
      }
      this.searching = false;
    }
  }
};
</script>

