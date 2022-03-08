import axios from 'axios'
// axios 的封装及请求、响应式拦截

export function request(config) {
  const instance = axios.create({
    baseURL:'/api',
    timeout: 5000, //请求最高5s
    method: config.method,
  })
  // 请求拦截
  instance.interceptors.request.use(config=>{
    // 如果有一些请求需要认证才可以访问， 搁这统一设置
    
    // 暂时不定义直接返回
    return config
  },
  err=>{
    console.log(err);
  }
  )
  // 响应拦截
  instance.interceptors.response.use(res=>{
    return res.data ? res.data : res;   // data有内容则返回
  },
  err=>{
    // 如果有需要授权才可以访问的接口， 统一去login授权

    // 如果有错误，这里会去处理， 显示错误信息
    console.log(err);
  }
  )
  return instance(config)
}