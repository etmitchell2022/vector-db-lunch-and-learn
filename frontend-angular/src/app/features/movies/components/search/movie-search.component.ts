import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-movie-search',
  templateUrl: './movie-search.component.html',
  standalone: true,
})
export class MovieSearchComponent {
  @Input() searchValue: string = '';
  @Output() searchValueChange = new EventEmitter<string>();
  @Output() submit = new EventEmitter<string>();

  onInputChange(event: Event) {
    const value = (event.target as HTMLTextAreaElement).value;
    this.searchValueChange.emit(value);
  }

  onSubmit() {
    this.submit.emit(this.searchValue);
  }
}
