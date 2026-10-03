export const SYMBOLS = ['cat', 'sun', 'sprout', 'star'];

export function createGame(random = Math.random) {
  const cards = [...SYMBOLS, ...SYMBOLS];
  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }
  const matched = new Set();
  let selected = [], moves = 0, locked = false;
  const snapshot = () => ({cards: [...cards], matched: [...matched], selected: [...selected], moves, locked, won: matched.size === cards.length});
  return {
    snapshot,
    flip(index) {
      if (!Number.isInteger(index) || index < 0 || index >= cards.length || locked || matched.has(index) || selected.includes(index)) return 'ignored';
      selected.push(index);
      if (selected.length === 1) return 'first';
      moves++;
      if (cards[selected[0]] === cards[selected[1]]) {
        selected.forEach(i => matched.add(i));
        selected = [];
        return matched.size === cards.length ? 'win' : 'match';
      }
      locked = true;
      return 'miss';
    },
    hideMismatch() {
      if (locked) { selected = []; locked = false; }
    }
  };
}
