import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';
import { WidgetComponent } from './widget/widget.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FlexLayoutModule } from '@angular/flex-layout';
import { PullRequestComponent } from './pull-request/pull-request.component';
import { JiraComponent } from './jira/jira.component';
import { BookmarksComponent } from './bookmarks/bookmarks.component';
import { BookmarkDropdownComponent } from './bookmark-dropdown/bookmark-dropdown.component';

@NgModule({
  declarations: [
    AppComponent,
    WidgetComponent,
    PullRequestComponent,
    JiraComponent,
    BookmarksComponent,
    BookmarkDropdownComponent
  ],
  imports: [
    BrowserModule,
    ServiceWorkerModule.register('/ngsw-worker.js', { enabled: environment.production }),
    NgbModule.forRoot(),
    FlexLayoutModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
