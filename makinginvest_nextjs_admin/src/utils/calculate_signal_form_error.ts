function getSignalFormErrorStopLoss(type: String, firstNumber: number | null | string, secondNumber: number | null | string) {
  if (firstNumber === null || secondNumber === null) return '';
  if (firstNumber === '' || secondNumber === '') return '';

  if (type === 'Long') {
    if (Number(firstNumber) <= Number(secondNumber)) return 'Stop loss must be lower than entry price';
  }

  if (type === 'Short') {
    if (Number(firstNumber) >= Number(secondNumber)) return 'Stop loss must be higher than entry price';
  }

  return '';
}

function getSignalFormErrorTakeProfit(type: String, firstNumber: number | null | string, secondNumber: number | null | string) {
  if (Number(firstNumber) === null || Number(secondNumber) === null) return '';
  if (firstNumber === null || firstNumber === '') return '';
  if (secondNumber === null || secondNumber === '') return '';

  if (type === 'Long') {
    if (Number(firstNumber) >= Number(secondNumber)) return 'Take profit must be higher than entry price';
  }

  if (type === 'Short') {
    if (Number(firstNumber) <= Number(secondNumber)) return 'Take profit must be lower than entry price';
  }

  return '';
}

export { getSignalFormErrorStopLoss, getSignalFormErrorTakeProfit };
