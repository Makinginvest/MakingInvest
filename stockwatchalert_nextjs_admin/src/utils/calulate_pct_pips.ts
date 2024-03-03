function calculatePctPips(firstNumber: number | null | string, secondNumber: number | null | string): string | number {
  if (firstNumber === null || secondNumber === null) return 0;
  if (firstNumber === '' || secondNumber === '') return 0;
  if (firstNumber === 0 || secondNumber === 0) return 0;

  const pips = Math.abs(Math.round((Number(firstNumber) - Number(secondNumber)) * 10000));

  let pct = ((Number(firstNumber) - Number(secondNumber)) / Number(firstNumber)) * 100;
  pct = Math.round((pct + Number.EPSILON) * 1000000) / 1000000;
  pct = Math.abs(pct);

  console.log(firstNumber, secondNumber, pct, pips);

  return `${pct}%  ||  ${pips} pips `;
}

export { calculatePctPips };
