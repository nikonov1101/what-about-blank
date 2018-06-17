import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  public topSites = [];

  // constructor() {
  //   if (chrome.topSites) {
  //     chrome.topSites.get(top => this.topSites = top);
  //   }
  // }

}
