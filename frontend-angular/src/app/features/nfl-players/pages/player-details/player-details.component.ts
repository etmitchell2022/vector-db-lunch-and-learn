import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-player-details',
  templateUrl: './player-details.component.html',
  imports: [],
  standalone: true,
})
export class PlayerDetailsPage {
  constructor(private route: ActivatedRoute) {}
  playerId: string = '';

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.playerId = params.get('id')!;
    });
  }
}
