module.exports = {   // 关闭严格模式
  lintOnSave:false, 
  devServer: {
    host:"0.0.0.0",
    port: '8080',
    // https: false
    open: true,
    // 以上的ip和端口时我们本机的，下面需要跨域的
    proxy: {
    // 配置跨域
      '/api': {
        target: 'http://localhost:8000',
        ws: true,
        changeOrigin: true, //允许跨域
        pathRewrite: {
          '^/api': ''  //请求时使用这个api就可以
        }
      }
    }
  }

}
