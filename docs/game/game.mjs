import {createGame} from './engine.mjs';

const $ = id => document.getElementById(id);
const board = $('board'), message = $('message');
const labels = {cat: 'pixel cat', sun: 'smiling sun', sprout: 'little sprout', star: 'happy star'};
let game, pending, generation = 0, best = null;
try {
  const saved = Number(localStorage.getItem('garden-pairs-best'));
  if (Number.isInteger(saved) && saved >= 4 && saved <= 10000) best = saved;
} catch { /* The game works when storage is unavailable. */ }

function draw() {
  const state = game.snapshot();
  $('moves').textContent = state.moves;
  $('pairs').innerHTML = `${state.matched.length / 2} <small>/ 4</small>`;
  $('best').textContent = best ?? '—';
  [...board.children].forEach((card, i) => {
    const matched = state.matched.includes(i), open = state.selected.includes(i);
    card.classList.toggle('open', open);
    card.classList.toggle('matched', matched);
    card.setAttribute('aria-pressed', String(open || matched));
    card.setAttribute('aria-disabled', String(matched));
    card.setAttribute('aria-label', `Card ${i + 1}, ${matched ? 'matched ' : ''}${matched || open ? labels[state.cards[i]] : 'face down'}`);
  });
}

function choose(index) {
  const outcome = game.flip(index);
  if (outcome === 'ignored') return;
  if (outcome === 'first') message.textContent = 'One little friend found. Where’s its pair?';
  if (outcome === 'match') message.textContent = 'A lovely little match! Keep growing.';
  if (outcome === 'miss') {
    message.textContent = 'Different little friends. Remember them and try again.';
    const round = generation;
    pending = setTimeout(() => {
      if (round !== generation) return;
      game.hideMismatch();
      message.textContent = 'Pick another pair. You’ve got this.';
      draw();
    }, 1050);
  }
  if (outcome === 'win') {
    const moves = game.snapshot().moves;
    const record = best === null || moves < best;
    if (record) {
      best = moves;
      try { localStorage.setItem('garden-pairs-best', String(best)); } catch {}
    }
    message.textContent = `Your garden is complete in ${moves} moves. ${record ? 'A new personal best!' : 'A little win for your day. :)'}`;
    message.classList.add('won');
  }
  draw();
}

function restart() {
  clearTimeout(pending);
  generation++;
  game = createGame();
  board.replaceChildren();
  game.snapshot().cards.forEach((symbol, i) => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'card';
    card.innerHTML = `<span class="back" aria-hidden="true">?</span><svg class="front" aria-hidden="true"><use href="#${symbol}"></use></svg>`;
    card.addEventListener('click', () => choose(i));
    board.append(card);
  });
  message.textContent = 'Pick any two cards. Let’s see what grows.';
  message.classList.remove('won');
  draw();
}

$('restart').addEventListener('click', restart);
$('theme').addEventListener('click', () => {
  const current = document.documentElement.dataset.theme ?? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.dataset.theme = current === 'dark' ? 'light' : 'dark';
  $('theme').setAttribute('aria-label', `Switch to ${current === 'dark' ? 'light' : 'dark'} theme`);
});
restart();
