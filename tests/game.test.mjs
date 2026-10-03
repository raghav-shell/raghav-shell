import test from 'node:test';
import assert from 'node:assert/strict';
import {createGame, SYMBOLS} from '../docs/game/engine.mjs';

test('every shuffled garden has exactly four pairs', () => {
  for (let attempt = 0; attempt < 100; attempt++) {
    const cards = createGame().snapshot().cards;
    assert.equal(cards.length, 8);
    for (const symbol of SYMBOLS) assert.equal(cards.filter(c => c === symbol).length, 2);
  }
});

test('invalid or repeated selections do not count moves or reveal extra cards', () => {
  const game = createGame(() => 0);
  for (const index of [-1, 8, 1.5, NaN]) assert.equal(game.flip(index), 'ignored');
  assert.equal(game.flip(0), 'first');
  assert.equal(game.flip(0), 'ignored');
  assert.equal(game.snapshot().moves, 0);
  assert.deepEqual(game.snapshot().selected, [0]);
});

test('a mismatch blocks a third selection until both cards are hidden', () => {
  const game = createGame(() => 0);
  const cards = game.snapshot().cards;
  const second = cards.findIndex(c => c !== cards[0]);
  game.flip(0);
  assert.equal(game.flip(second), 'miss');
  assert.equal(game.flip((second + 1) % 8), 'ignored');
  assert.equal(game.snapshot().moves, 1);
  assert.equal(game.snapshot().locked, true);
  game.hideMismatch();
  assert.deepEqual(game.snapshot().selected, []);
  assert.equal(game.snapshot().locked, false);
  assert.equal(game.flip(0), 'first');
});

test('four matched pairs win in four moves and cannot be counted twice', () => {
  const game = createGame(() => .5);
  const cards = game.snapshot().cards;
  for (const [index, symbol] of SYMBOLS.entries()) {
    const pair = cards.flatMap((c, i) => c === symbol ? [i] : []);
    assert.equal(game.flip(pair[0]), 'first');
    assert.equal(game.flip(pair[1]), index === 3 ? 'win' : 'match');
    assert.equal(game.flip(pair[0]), 'ignored');
  }
  assert.equal(game.snapshot().moves, 4);
  assert.equal(game.snapshot().won, true);
  assert.equal(game.snapshot().matched.length, 8);
});

test('a fresh game discards previous selections and score', () => {
  const first = createGame();
  first.flip(0); first.flip(1);
  const fresh = createGame();
  assert.deepEqual(fresh.snapshot().matched, []);
  assert.deepEqual(fresh.snapshot().selected, []);
  assert.equal(fresh.snapshot().moves, 0);
  assert.equal(fresh.snapshot().locked, false);
});
