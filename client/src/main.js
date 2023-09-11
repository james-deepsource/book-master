import './tailwind.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import ToastContainer from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';

const app = createApp(App);

// Register vue-toast-notification
app.use(ToastContainer);

app.use(router)

app.mount('#app')
