export function combineDateAndTime(date: Date | null, time: Date | null): Date | null {
  if (!date || !time) return null;
  const dateClone = new Date(date.getTime());
  dateClone.setHours(time.getHours(), time.getMinutes());
  return dateClone;
}
