import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NFLPlayerSearchResult, NflPlayersService } from '../../../../api';
import { calculateYearsInLeague } from '../../../../utils/calculateYearsInLeague';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-player-details',
  templateUrl: './player-details.component.html',
  imports: [DecimalPipe],
  standalone: true,
})
export class PlayerDetailsPage {
  constructor(
    private route: ActivatedRoute,
    private playerService: NflPlayersService
  ) {}
  playerId: string = '';
  player: NFLPlayerSearchResult | undefined;
  isLoading = false;

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.playerId = params.get('id')!;
      this.fetchPlayer();
    });
  }

  fetchPlayer() {
    console.log('fetching player', this.playerId);
    this.isLoading = true;
    this.playerService.apiV1PlayersPlayerIdGet(this.playerId).subscribe({
      next: (player) => {
        this.player = player;
        this.isLoading = false;
        console.log('player', player);
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error fetching player', err);
      },
    });
  }

  get yearsInLeague(): number {
    return calculateYearsInLeague(this.player?.debut_year);
  }
}
