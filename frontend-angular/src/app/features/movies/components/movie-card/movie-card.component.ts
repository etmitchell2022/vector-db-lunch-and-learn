import { Component, Input } from '@angular/core';
import { Movie } from '../../../../api';
import { DecimalPipe, UpperCasePipe } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-movie-card',
  templateUrl: './movie-card.component.html',
  standalone: true,
  imports: [DecimalPipe, UpperCasePipe, RouterModule],
})
export class MovieCardComponent {
  @Input({ required: true }) movie: Movie = {};
}
