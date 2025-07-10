import { Component, CUSTOM_ELEMENTS_SCHEMA, signal } from '@angular/core';
import { PlayerSearchComponent } from '../../components/player-search/player-search.component';
import { NFLPlayerSearchResult, NflPlayersService } from '../../../../api';
import { BadgeComponent } from '../../../../shared/components/badge.component';
import { PlayerCardComponent } from '../../components/player-card/player-card.component';

@Component({
  selector: 'app-players',
  templateUrl: './players.component.html',
  standalone: true,
  imports: [PlayerSearchComponent, BadgeComponent, PlayerCardComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class PlayersPage {
  constructor(private playerService: NflPlayersService) {}

  isLoading = false;
  recommendedSearches = [
    'Mobile QB with Strong arm',
    'Efficient pocket passer',
    'Powerful running back',
    'Underrated WR with great hands',
    'Find RBs who are explosive runners AND effective in the pass game.',
    'Find a WR with elite speed and deep-threat ability but more consistent hands.',
    'Dual-threat QB with 600+ rushing yards',
  ];
  searchValue = signal('');
  players = signal<NFLPlayerSearchResult[]>([]);

  handleSearch(value: string) {
    console.log('Search submitted', value);
    if (!value) return;
    this.isLoading = true;
    this.players.set([]);

    this.searchValue.set(value);
    this.playerService
      .apiV1PlayersSimilaritySearchPost({ search: value })
      .subscribe({
        next: (players) => {
          console.log('players', players);
          this.players.set(players);
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Error fetching players', err);
          this.isLoading = false;
        },
      });
  }
}
