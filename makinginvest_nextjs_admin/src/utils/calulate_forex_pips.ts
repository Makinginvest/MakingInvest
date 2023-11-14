function calculateForexPips(firstNumber: number | null | string, secondNumber: number | null | string): number {
  if (firstNumber === null || secondNumber === null) return 0;
  if (firstNumber === '' || secondNumber === '') return 0;
  if (firstNumber === 0 || secondNumber === 0) return 0;

  return Math.abs(Math.round((Number(firstNumber) - Number(secondNumber)) * 10000));
}

export { calculateForexPips };
