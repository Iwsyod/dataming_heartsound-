<template>
  <div>
    <h2>上传心音wav文件</h2>
    <input type="file" @change="handleFileChange" accept=".wav">
    <button @click="submitFile">上传</button>
    <p v-if="uploadResult === null">正在分类，请稍候...</p>
    <p v-else-if="uploadResult.code === 0">分类结果：{{ uploadResult.stdout }}</p>
    <p v-else>分类失败，请重试</p>
    <router-link to="/NavBar_">返回上级</router-link>
  </div>
  <nav>
    <router-link to="/_">返回上级</router-link>
    <router-link to="/">退出登录</router-link>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
      uploadResult: null,
    };
  },
  methods: {
    handleFileChange(e) {
      this.file = e.target.files[0];
    },
    async submitFile() {
      if (!this.file) {
        alert('请先选择一个文件');
        return;
      }
      const formData = new FormData();
      formData.append('wav', this.file);
      try {
        const response = await axios.post('/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.uploadResult = response.data;
      } catch (error) {
        console.error('上传失败', error);
        this.uploadResult = { code: -1 };
      }
    },
  },
};
</script>

<style scoped>
/* 添加一些样式 */
</style>
