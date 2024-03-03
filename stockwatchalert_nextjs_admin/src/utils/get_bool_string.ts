export function getStringFromBool(isActive?: boolean) {
  if (isActive === undefined || isActive === null) return 'Yes';
  return isActive === true ? 'Yes' : 'No';
}

export function getBoolFromString(isActive?: string) {
  if (isActive == 'Yes') return true;
  return false;
}
