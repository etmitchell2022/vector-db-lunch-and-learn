import { Component, Input } from '@angular/core';
import { NFLPlayerSearchResult } from '../../../../api';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-runningback-card-stats',
  templateUrl: './runningback-card-stats.component.html',
  imports: [DecimalPipe],
  standalone: true,
})
export class RunningBackCardStatsComponent {
  constructor() {}
  @Input() player!: NFLPlayerSearchResult;
}
