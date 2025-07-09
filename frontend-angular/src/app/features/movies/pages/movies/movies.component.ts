import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BadgeComponent } from '../../../../shared/components/badge.component';
import { MovieSearchComponent } from '../../components/search/movie-search.component';
import { Movie, MoviesService } from '../../../../api';
import { MovieCardComponent } from '../../components/movie-card/movie-card.component';
import { MovieSearchService } from '../../services/movie-search.service';

@Component({
  selector: 'app-movies',
  templateUrl: './movies.component.html',
  imports: [BadgeComponent, MovieSearchComponent, MovieCardComponent],
  standalone: true,
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class MoviesPage {
  constructor(
    private movieService: MoviesService,
    private movieSearchService: MovieSearchService
  ) {}

  mockMovieSearches = [
    'Intense action with lots of explosions and car chases',
    'A movie about the future',
    'Underdog sports team overcoming impossible odds',
    'Comedy about a group of friends',
  ];
  searchValue: string = '';

  isLoading = false;
  movies: Movie[] = [];

  handleSearch(value: string) {
    if (!value) return;
    this.isLoading = true;
    this.movies = [];

    this.movieService.apiV1MoviesSearchPost({ search: value }).subscribe({
      next: (movies) => {
        this.movies = movies;
        this.movieSearchService.setSearch(value, movies);
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error fetching movies', err);
        this.isLoading = false;
      },
    });
  }

  ngOnInit(): void {
    // Restore previous search state if available
    this.searchValue = this.movieSearchService.searchValue;
    this.movies = this.movieSearchService.searchResults;
  }
}
