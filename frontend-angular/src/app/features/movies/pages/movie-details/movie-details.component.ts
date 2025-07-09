import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Movie, MoviesService } from '../../../../api';
import { DecimalPipe, UpperCasePipe } from '@angular/common';
import { MovieCardComponent } from '../../components/movie-card/movie-card.component';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  standalone: true,
  imports: [DecimalPipe, UpperCasePipe, MovieCardComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class MovieDetailsPage {
  constructor(
    private route: ActivatedRoute,
    private movieService: MoviesService
  ) {}

  movieId: string = '';
  isLoading = false;
  isFetchingRecommendedMovies = false;
  movie: Movie | undefined;
  recommendedMovies: Movie[] = [];

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.movieId = params.get('id')!;
      this.fetchMovie();
    });
  }

  fetchMovie() {
    this.isLoading = true;
    this.isFetchingRecommendedMovies = true;

    this.movieService.apiV1MoviesMovieMovieIdGet(this.movieId).subscribe({
      next: (movie) => {
        this.movie = movie;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error fetching movie', err);
        this.isLoading = false;
      },
    });

    this.movieService
      .apiV1MoviesMovieMovieIdRecommendationsGet(this.movieId)
      .subscribe({
        next: (movies) => {
          this.recommendedMovies = movies || [];
          this.isFetchingRecommendedMovies = false;
          console.log('recommended movies', movies);
        },
        error: (err) => {
          console.error('Error fetching recommended movies', err);
          this.isFetchingRecommendedMovies = false;
          this.recommendedMovies = [];
        },
      });
  }
}
