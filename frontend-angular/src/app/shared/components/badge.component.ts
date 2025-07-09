import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-badge',
  templateUrl: './badge.component.html',
  standalone: true,
})
export class BadgeComponent {
  @Input() text = '';
  @Output() badgeClicked = new EventEmitter<string>();

  handleClick() {
    this.badgeClicked.emit(this.text);
  }
}
