import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { NgbDropdown } from '@ng-bootstrap/ng-bootstrap';
import { Bookmark } from '../../dto/bookmark';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-bookmark-dropdown',
  templateUrl: './bookmark-dropdown.component.html',
  styleUrls: ['./bookmark-dropdown.component.scss']
})
export class BookmarkDropdownComponent implements OnInit {
  @ViewChild('drop') drop: NgbDropdown;
  @Input('items') items: Bookmark[];
  @Input('placement') placement;

  constructor(private sanitizer: DomSanitizer) {
  }

  ngOnInit() {
    if (!this.placement) {
      this.placement = 'right-top';
    }
  }

  open() {
    this.drop.open();
  }

  close() {
    this.drop.close();
  }

  getUrl(url) {
    return this.sanitizer.bypassSecurityTrustUrl('chrome://favicon/' + url);
  }
}
