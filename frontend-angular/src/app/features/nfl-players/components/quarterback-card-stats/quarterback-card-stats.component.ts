import { Component, Input } from '@angular/core';
import { NFLPlayerSearchResult } from '../../../../api';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-quarterback-card-stats',
  templateUrl: './quarterback-card-stats.component.html',
  imports: [DecimalPipe],
  standalone: true,
})
export class QuarterbackCardStatsComponent {
  constructor() {}
  @Input() player!: NFLPlayerSearchResult;
}
