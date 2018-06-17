import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';
import { environment } from './environments/environment';

if (environment.production) {
  enableProdMode();
}

const html = localStorage.getItem('html');
if (html) {
  document.body.innerHTML = html;
}

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.log(err));
