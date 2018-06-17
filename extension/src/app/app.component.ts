import { AfterViewInit, Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements AfterViewInit {
  public topSites = [];

  ngAfterViewInit(): void {
    localStorage.setItem('html', document.body.innerHTML);
  }
}