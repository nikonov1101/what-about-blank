import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Bookmark } from '../../dto/bookmark';

@Component({
  selector: 'app-bookmarks',
  templateUrl: './bookmarks.component.html',
  styleUrls: ['./bookmarks.component.scss']
})
export class BookmarksComponent implements OnInit {
  bookmarks: Bookmark[];

  constructor(private sanitizer: DomSanitizer) {
  }

  ngOnInit() {
    (window as any).chrome.bookmarks.getSubTree('1', bookmarks => {
      this.bookmarks = bookmarks[0].children;
    });
  }

  getUrl(url) {
    return this.sanitizer.bypassSecurityTrustUrl('chrome://favicon/' + url);
  }

}
