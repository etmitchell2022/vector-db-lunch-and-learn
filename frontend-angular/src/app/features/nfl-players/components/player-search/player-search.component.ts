import { Component, EventEmitter, Input, Output, signal } from "@angular/core";


@Component({
  selector: "app-player-search",
  templateUrl: "./player-search.component.html",
  standalone: true,
  imports: [],
})
export class PlayerSearchComponent {
  constructor() { }

  private _searchValueInput = "";
  searchValueSignal = signal("")

  @Input()
  set searchValue(value: string) {
    this._searchValueInput = value;
    this.searchValueSignal.set(value);
  }
  get searchValue() {
    return this._searchValueInput
  }

  @Output() submit = new EventEmitter<string>();

  onInputChange(event: Event) {
    const value = (event.target as HTMLTextAreaElement).value;
    this.searchValueSignal.set(value);
  }

  onSubmit() {
    this.submit.emit(this.searchValueSignal());
  }
}
