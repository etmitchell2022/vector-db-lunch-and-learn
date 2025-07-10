import { Component, Input } from '@angular/core';
import { NFLPlayerSearchResult } from '../../../../api';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-wr-card-stats',
  templateUrl: './wr-card-stats.component.html',
  imports: [DecimalPipe],
  standalone: true,
})
export class WRCardStatsComponent {
  constructor() {}
  @Input() player!: NFLPlayerSearchResult;
}
