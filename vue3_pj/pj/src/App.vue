<template>
  <!-- <router-view/> -->
  <div>
    <router-link to="/login">登录</router-link>
    <router-view/>
  </div>
</template>

<script>
import {onMounted, reactive} from 'vue'
import {request} from './network/request'
export default {
  setup(){
    return {
    }
  },

}
</script>
