properCase(String? s) {
  if (s == null) return '';
  return s.split(' ').map((str) => str[0].toUpperCase() + str.substring(1)).join(' ');
}
