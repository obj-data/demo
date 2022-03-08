<template>
  <div>
    请输入用户名:<input type="text" v-model="user.username"><br>
     请输入密码:<input type=" text" v-model="user.password"><br>
      <button @click="login">登录</button>
  </div>
</template>

<script>
import { request } from '../network/request'
import {ref} from 'vue'
// import {useCookies} from 'vue3-cookies'
import axios from 'axios'
export default {
  setup(props) {  
    let user = {
      username: '',
      password: ''
    }
    // const {cookies} = useCookies()

    function login() {

     axios.post(
       '/api/login/',user,{
     }).then(res=>{
       localStorage.setItem('token', res.data)
       axios.post('/api/blog/userblog/',{'title': `这是${user.username}的博客`, 'body': 'test123456'})
     })
    }
    // axios.post('/api')
    return {
      user,
      login
    }
  }
  
}
</script>