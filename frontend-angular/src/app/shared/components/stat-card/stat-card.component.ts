import { Component, Input } from '@angular/core';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-stat-card',
  templateUrl: './stat-card.component.html',
  imports: [DecimalPipe],
  standalone: true,
})
export class StatCardComponent {
  @Input() value: number | string | null | undefined;
  @Input() label: string = '';
  @Input() isPercentage: boolean = false;
  @Input() useThousandsSeparator: boolean = false;
  @Input() decimalPlaces: string = '1.1-1';

  get formattedValue(): string {
    if (this.value === null || this.value === undefined) {
      return '-';
    }

    if (this.isPercentage) {
      return `${this.value}%`;
    }

    return this.value.toString();
  }
}
