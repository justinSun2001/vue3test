import Storage from './storage';
const storage = Storage.getInstance();
storage.setItem('key', 'value');
console.log(storage.getItem('key'));