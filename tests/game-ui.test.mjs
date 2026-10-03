import test from 'node:test';
import assert from 'node:assert/strict';

test('game controller handles winning, storage failures, themes, and stale restart timers', async () => {
  const elements = new Map();
  class Element {
    children = []; attributes = {}; handlers = {}; textContent = ''; innerHTML = '';
    classes = new Set();
    classList = {toggle: (name, value) => value ? this.classes.add(name) : this.classes.delete(name), add: name => this.classes.add(name), remove: name => this.classes.delete(name)};
    setAttribute(name, value) {this.attributes[name] = value;}
    addEventListener(name, action) {this.handlers[name] = action;}
    replaceChildren() {this.children = [];}
    append(child) {this.children.push(child);}
    click() {this.handlers.click();}
  }
  const saved = Object.fromEntries(['document', 'localStorage', 'matchMedia', 'setTimeout', 'clearTimeout'].map(k => [k, globalThis[k]]));
  const timers = new Map(); let serial = 0;
  try {
    globalThis.document = {getElementById: id => {if (!elements.has(id)) elements.set(id, new Element());return elements.get(id);}, createElement: () => new Element(), documentElement: {dataset: {}}};
    globalThis.localStorage = {getItem() {throw Error('storage blocked');}, setItem() {throw Error('storage blocked');}};
    globalThis.matchMedia = () => ({matches: false});
    globalThis.setTimeout = fn => {timers.set(++serial, fn); return serial;};
    globalThis.clearTimeout = id => timers.delete(id);
    await import('../docs/game/game.mjs');
    const board = elements.get('board');
    assert.equal(board.children.length, 8);
    const pairs = new Map();
    board.children.forEach(card => {const symbol = card.innerHTML.match(/href="#([a-z]+)"/)[1];if (!pairs.has(symbol)) pairs.set(symbol, []);pairs.get(symbol).push(card);});
    for (const pair of pairs.values()) {pair[0].click();pair[1].click();}
    assert.equal(elements.get('moves').textContent, 4);
    assert.equal(elements.get('best').textContent, 4);
    assert.ok(elements.get('message').textContent.includes('garden is complete'));
    assert.ok(board.children.every(c => c.attributes['aria-disabled'] === 'true'));
    elements.get('theme').click();
    assert.equal(document.documentElement.dataset.theme, 'dark');
    elements.get('restart').click();
    const oldCards = [...board.children];
    const first = oldCards[0].innerHTML;
    const different = oldCards.find(c => c.innerHTML !== first);
    oldCards[0].click(); different.click();
    assert.equal(timers.size, 1);
    const stale = [...timers.values()][0];
    elements.get('restart').click();
    assert.equal(timers.size, 0);
    board.children[0].click();
    stale();
    assert.equal(elements.get('moves').textContent, 0);
    assert.equal(board.children[0].attributes['aria-pressed'], 'true');
  } finally {for (const [key, value] of Object.entries(saved)) {if (value === undefined) delete globalThis[key];else globalThis[key] = value;}}
});
