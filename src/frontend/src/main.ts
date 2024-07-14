import { createApp } from "vue";
import App from "./App.vue";

/* import the fontawesome core */
import { IconDefinition, library } from "@fortawesome/fontawesome-svg-core";

/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

/* import specific icons */
import * as faBrands from "@fortawesome/free-brands-svg-icons";
import * as faSolid from "@fortawesome/free-solid-svg-icons";
import * as faRegular from "@fortawesome/free-regular-svg-icons";

/* add the imported icons to the library */
for (const icon of Object.values(faBrands)) {
  if (icon.hasOwnProperty("iconName")) {
    library.add(icon as IconDefinition);
  }
}
for (const icon of Object.values(faSolid)) {
  if (icon.hasOwnProperty("iconName")) {
    library.add(icon as IconDefinition);
  }
}
for (const icon of Object.values(faRegular)) {
  if (icon.hasOwnProperty("iconName")) {
    library.add(icon as IconDefinition);
  }
}

createApp(App).component("font-awesome-icon", FontAwesomeIcon).mount("#app");
