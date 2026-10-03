import './style.css';
import { judgeTapSequence, makeRound, resetCurrentSequence } from './logic.js';

const root = document.querySelector('#app');
const symbols = { sun: '☀', moon: '☾', star: '✦' };
let state = { target: makeRound(), picks: [], score: 0, hearts: 3, message: 'Tap the symbols in order.' };

function render() {
  root.innerHTML = `
    <main class="shell"><section class="phone">
      <header><p class="eyebrow">OPTIMIND · GAME STARTER</p><h1>Sequence Lab</h1>
      <div class="hud"><span>❤ ${state.hearts}</span><span>★ ${state.score}</span></div></header>
      <p class="hint">Tap in this order</p>
      <div class="target">${state.target.map(x => `<span>${symbols[x]}</span>`).join('')}</div>
      <p class="hint">Your taps</p>
      <div class="selected">${state.picks.map(x => `<span>${symbols[x]}</span>`).join('') || '○ ○ ○'}</div>
      <p class="message" role="status">${state.message}</p>
      <div class="controls">${Object.keys(symbols).map(k => `<button type="button" data-piece="${k}" ${state.hearts === 0 ? 'disabled' : ''}>${symbols[k]}</button>`).join('')}</div>
      <div class="actions"><button type="button" data-action="reset">Clear current picks</button><button type="button" data-action="new">New game</button></div>
      <footer>Mobile portrait · desktop centered · starter only</footer>
    </section></main>`;
}

function pick(piece) {
  if (state.hearts === 0 || state.picks.length >= state.target.length) return;
  state = {...state, picks: [...state.picks, piece]};
  const result = judgeTapSequence(state.picks, state.target);
  if (result === 'correct') state = {...state, score: state.score + 10, picks: [], target: makeRound(), message: 'Success! +10 points.'};
  else if (result === 'wrong') state = {...state, hearts: state.hearts - 1, picks: [], message: state.hearts - 1 ? 'Wrong sequence. Try again.' : 'Game over.'};
  else state.message = 'Keep going…';
  render();
}
root.addEventListener('click', event => {
  const button = event.target.closest('button');
  if (!button || !root.contains(button)) return;
  if (button.dataset.piece) pick(button.dataset.piece);
  else if (button.dataset.action === 'reset') { state = resetCurrentSequence(state); state.message = 'Picks cleared.'; render(); }
  else if (button.dataset.action === 'new') { state = { target: makeRound(), picks: [], score: 0, hearts: 3, message: 'New game started.' }; render(); }
});
render();
