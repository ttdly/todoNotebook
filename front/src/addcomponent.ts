import type { App } from 'vue';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import ScrollPanel from 'primevue/scrollpanel';
import Card from 'primevue/card';
import Textarea from 'primevue/textarea';
import Dialog from 'primevue/dialog';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import Dropdown from 'primevue/dropdown';
import Tooltip from 'primevue/tooltip';
import RadioButton from 'primevue/radiobutton';
import Rating from 'primevue/rating';


export function AddPrimComponent(app: App) {
  app.directive('tooltip', Tooltip);
  app.component('Button', Button);
  app.component('InputText', InputText);
  app.component('Card', Card);
  app.component('Textarea', Textarea);
  app.component('Dialog', Dialog);
  app.component('InputGroupAddon', InputGroupAddon);
  app.component('InputGroup', InputGroup);
  app.component('ScrollPanel', ScrollPanel);
  app.component('Dropdown', Dropdown);
  app.component('RadioButton', RadioButton)
  app.component('Rating', Rating)
}
