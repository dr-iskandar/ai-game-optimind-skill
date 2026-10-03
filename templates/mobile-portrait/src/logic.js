/** Pure demo mechanics, not the specific game described by a user's approved spec. */
export function judgeTapSequence(picks, target) {
  if (picks.length < target.length) return 'in-progress';
  if (picks.length > target.length) return 'wrong';
  return picks.every((x, i) => x === target[i]) ? 'correct' : 'wrong';
}
export function makeRound(random = Math.random) {
  const values = ['sun', 'moon', 'star'];
  for (let i = values.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [values[i], values[j]] = [values[j], values[i]];
  }
  return values;
}
export function resetCurrentSequence(state) { return { ...state, picks: [] }; }
