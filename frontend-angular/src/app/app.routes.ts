import { Routes } from '@angular/router';
import { MoviesPage } from './features/movies/pages/movies/movies.component';
import { MovieDetailsPage } from './features/movies/pages/movie-details/movie-details.component';
import { PlayersPage } from './features/nfl-players/pages/players/players.component';
import { PlayerDetailsPage } from './features/nfl-players/pages/player-details/player-details.component';

export const routes: Routes = [
  {
    path: 'movies',
    component: MoviesPage,
  },
  { path: 'movies/:id', component: MovieDetailsPage },
  { path: 'nfl-players', component: PlayersPage },
  { path: 'nfl-players/:id', component: PlayerDetailsPage },
];
