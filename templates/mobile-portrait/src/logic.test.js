import { test } from 'node:test';
import assert from 'node:assert/strict';
import { judgeTapSequence, makeRound, resetCurrentSequence } from './logic.js';
test('sequence incomplete, correct, wrong', () => {
  assert.equal(judgeTapSequence(['sun'], ['sun', 'moon']), 'in-progress');
  assert.equal(judgeTapSequence(['sun','moon'], ['sun','moon']), 'correct');
  assert.equal(judgeTapSequence(['moon','sun'], ['sun','moon']), 'wrong');
});
test('reset clears picks only', () => {
  const state = { score: 20, hearts: 3, time: 44, target:['sun'], picks:['moon'] };
  const next = resetCurrentSequence(state);
  assert.deepEqual(next.picks, []);
  assert.equal(next.score,20);
  assert.equal(next.hearts,3);
  assert.equal(next.time,44);
  assert.equal(next.target,state.target);
});
test('round includes each symbol once', () => {
  assert.deepEqual(new Set(makeRound(() => 0.5)), new Set(['sun','moon','star']));
});
