export function calculateYearsInLeague(debutYear: string | number | null | undefined): number {
  const currentYear = new Date().getFullYear();
  const debut = Number(debutYear);
  if (!debutYear || isNaN(debut) || debut > currentYear) return 0;
  return currentYear - debut;
}
