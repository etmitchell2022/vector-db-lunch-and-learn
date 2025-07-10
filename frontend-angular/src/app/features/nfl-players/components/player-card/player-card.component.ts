import { Component, Input } from '@angular/core';
import { NFLPlayerSearchResult } from '../../../../api';
import { trigger, transition, style, animate } from '@angular/animations';
import { DecimalPipe } from '@angular/common';
import { calculateYearsInLeague } from '../../../../utils/calculateYearsInLeague';
import { QuarterbackCardStatsComponent } from '../quarterback-card-stats/quarterback-card-stats.component';
import { RunningBackCardStatsComponent } from '../runningback-card-stats/runningback-card-stats.component';
import { WRCardStatsComponent } from '../wr-card-stats/wr-card-stats.component';

@Component({
  selector: 'app-player-card',
  templateUrl: './player-card.component.html',
  standalone: true,
  imports: [
    DecimalPipe,
    QuarterbackCardStatsComponent,
    RunningBackCardStatsComponent,
    WRCardStatsComponent,
  ],
  animations: [
    trigger('slideInOut', [
      transition(':enter', [
        style({ height: 0, opacity: 0 }),
        animate('300ms ease-out', style({ height: '*', opacity: 1 })),
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({ height: 0, opacity: 0 })),
      ]),
    ]),
  ],
})
export class PlayerCardComponent {
  constructor() {}
  @Input() player!: NFLPlayerSearchResult;
  @Input() index!: number;
  showVectorAnalysis = false;

  get similarityPercent(): string {
    const sim = this.player?.similarity ?? 0;
    return `${(sim * 100).toFixed(1)}%`;
  }

  get yearsInLeague(): number {
    return calculateYearsInLeague(this.player?.debut_year);
  }

  get shortenedEmbeddings(): string {
    if (!this.player?.embedding) return '';
    const embeddings = this.player?.embedding;
    const roundedEmbeddings = embeddings.map((emb: number) => emb.toFixed(4));
    const embeddingStr = roundedEmbeddings.slice(0, 15).join(', ') ?? '';
    return `[${embeddingStr}, ...]`;
  }

  get borderColor() {
    if (this.index === 0) return 'border-l-green-500';
    if (this.index > 0) return 'border-l-yellow-500';
    return 'border-l-red-500';
  }
  toggleVectorAnalysis() {
    this.showVectorAnalysis = !this.showVectorAnalysis;
  }
}
