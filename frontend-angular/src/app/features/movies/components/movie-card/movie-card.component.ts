import { Component, Input } from '@angular/core';
import { Movie } from '../../../../api';
import { DecimalPipe, UpperCasePipe } from '@angular/common';
import { RouterModule } from '@angular/router';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-movie-card',
  templateUrl: './movie-card.component.html',
  standalone: true,
  imports: [DecimalPipe, UpperCasePipe, RouterModule],
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
export class MovieCardComponent {
  @Input({ required: true }) movie: Movie = {};
  showVectorAnalysis = false;

  get shortenedEmbeddings(): string {
    if (!this.movie?.embedding) return '';
    const embeddings = this.movie?.embedding;
    const roundedEmbeddings = embeddings.map((emb: number) => emb.toFixed(4));
    const embeddingStr = roundedEmbeddings.slice(0, 15).join(', ') ?? '';
    return `[${embeddingStr}, ...]`;
  }

  toggleVectorAnalysis() {
    this.showVectorAnalysis = !this.showVectorAnalysis;
  }
}
