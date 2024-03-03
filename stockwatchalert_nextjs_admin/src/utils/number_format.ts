export function numToPrecision(num: number, precision = 0) {
  return Number(num.toFixed(precision));
}

export function numToPercent(num: number) {
  return numToPrecision(num * 100, 2) + '%';
}
