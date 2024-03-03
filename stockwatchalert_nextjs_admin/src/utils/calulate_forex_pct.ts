function calculateForexPct(firstNumber: number | null, secondNumber: number | null): number {
  if (firstNumber === null || secondNumber === null) return 0;
  if (firstNumber === 0 || secondNumber === 0) return 0;

  return Math.abs(firstNumber - secondNumber) / secondNumber;
}

export { calculateForexPct };
