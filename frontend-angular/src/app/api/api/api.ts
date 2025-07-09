export * from './movies.service';
import { MoviesService } from './movies.service';
export * from './nflPlayers.service';
import { NflPlayersService } from './nflPlayers.service';
export * from './ping.service';
import { PingService } from './ping.service';
export const APIS = [MoviesService, NflPlayersService, PingService];
