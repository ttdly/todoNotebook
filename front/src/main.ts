import './assets/main.css';
import 'primeicons/primeicons.css';
import 'primevue/resources/themes/aura-light-green/theme.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import PrimeVue from 'primevue/config';
import { AddPrimComponent } from './addcomponent';

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import Prism from 'prismjs';
import 'prismjs/components/prism-json';
VMdPreview.use(githubTheme, {
  Prism,
});


const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(PrimeVue);
app.use(VMdPreview);

AddPrimComponent(app);

app.mount('#app');
