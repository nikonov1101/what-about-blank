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
    this.loadCachedBookmarks();

    (window as any).chrome.bookmarks.getSubTree('1', bm => {
      const bookmarks = bm[0].children;
      this.bookmarks = bookmarks;
      localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
    });
  }

  getUrl(url) {
    return this.sanitizer.bypassSecurityTrustUrl('chrome://favicon/' + url);
  }

  private loadCachedBookmarks() {
    let bookmarks = [];
    try {
      bookmarks = <Bookmark[]>JSON.parse(localStorage.getItem('bookmarks'));
    } catch (e) {
      console.error('Error while get bookmarks from cache', e);
    } finally {
      this.bookmarks = bookmarks;
    }
  }
}
