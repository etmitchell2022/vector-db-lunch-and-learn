import { Injectable } from '@angular/core';
import { Movie } from '../../../api';

@Injectable({
  providedIn: 'root',
})
export class MovieSearchService {
  searchValue: string = '';
  searchResults: Movie[] = [];

  setSearch(query: string, results: Movie[]) {
    this.searchValue = query;
    this.searchResults = results;
  }

  clear() {
    this.searchValue = '';
    this.searchResults = [];
  }
}
