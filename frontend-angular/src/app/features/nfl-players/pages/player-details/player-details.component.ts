import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NFLPlayerSearchResult, NflPlayersService, NFLPlayerVectorVisualization } from '../../../../api';
import { calculateYearsInLeague } from '../../../../utils/calculateYearsInLeague';
import { DecimalPipe } from '@angular/common';
import { StatCardComponent } from '../../../../shared/components/stat-card/stat-card.component';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js';

@Component({
  selector: 'app-player-details',
  templateUrl: './player-details.component.html',
  imports: [DecimalPipe, StatCardComponent, BaseChartDirective],
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
  similarPlayers: NFLPlayerVectorVisualization[] = [];
  isLoadingChart = false;

  // Chart configuration
  public scatterChartType = 'scatter' as const;
  public scatterChartData: ChartData<'scatter'> = {
    datasets: []
  };
  public scatterChartOptions: ChartConfiguration<'scatter'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Player Similarity Visualization'
      },
      legend: {
        display: true,
        position: 'top'
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'X Coordinate'
        },
        grid: {
          display: false
        }
      },
      y: {
        title: {
          display: true,
          text: 'Y Coordinate'
        },
        grid: {
          display: false
        }
      }
    }
  };

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
        
        // Fetch vector visualization data
        this.fetchVectorVisualization();
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error fetching player', err);
      },
    });
  }

  fetchVectorVisualization() {
    if (!this.playerId) return;
    
    this.isLoadingChart = true;
    this.playerService.apiV1PlayersPlayerIdVectorVisualizationGet(this.playerId).subscribe({
      next: (similarPlayers) => {
        this.similarPlayers = similarPlayers;
        this.isLoadingChart = false;
        console.log('similar players', similarPlayers);
        
        // Update chart data
        this.updateChartData();
      },
      error: (err) => {
        this.isLoadingChart = false;
        console.error('Error fetching vector visualization', err);
      },
    });
  }

  updateChartData() {
    if (!this.similarPlayers || this.similarPlayers.length === 0) return;

    // Find the current player in the similar players data
    const currentPlayer = this.similarPlayers.find(p => p.id === this.playerId);
    const otherPlayers = this.similarPlayers.filter(p => p.id !== this.playerId);

    const datasets = [];

    // Add current player as a special dataset
    if (currentPlayer && currentPlayer.coordinates) {
      datasets.push({
        label: 'Current Player',
        data: [{
          x: currentPlayer.coordinates.x || 0,
          y: currentPlayer.coordinates.y || 0
        }],
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        pointRadius: 8,
        pointHoverRadius: 10
      });
    }

    // Add similar players
    if (otherPlayers.length > 0) {
      datasets.push({
        label: 'Similar Players',
        data: otherPlayers
          .filter(p => p.coordinates && p.coordinates.x !== undefined && p.coordinates.y !== undefined)
          .map(p => ({
            x: p.coordinates!.x!,
            y: p.coordinates!.y!
          })),
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgba(59, 130, 246, 1)',
        pointRadius: 6,
        pointHoverRadius: 8
      });
    }

    this.scatterChartData = {
      datasets: datasets
    };
  }

  get yearsInLeague(): number {
    return calculateYearsInLeague(this.player?.debut_year);
  }
}
