import { createApp } from "vue";
import { createPinia } from "pinia";
import { useAuthStore } from "@/stores/auth";
import App from "./App.vue";
import router from "./router";
import "./assets/base.css";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faChevronLeft,
  faChevronRight,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faChevronLeft, faChevronRight);

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.component("font-awesome-icon", FontAwesomeIcon);

const authStore = useAuthStore();
authStore.initAuth().finally(() => {
  app.mount("#app");
});
