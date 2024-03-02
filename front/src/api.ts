import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000/api';
const TODO = `${BASE_URL}/todo`;
const TODO_INFO = `${TODO}/info`;
const TODO_NOTE = `${TODO}/note`;
const DATE_NOTE = `${BASE_URL}/date/note`;

export type TodoObj = {
  title: string;
  createDate: string;
  state: number;
  completeDate: string;
  level:number;
  hashCode:string;
};

export async function createTodoApi(todo: TodoObj) {
  return await axios.post(TODO, todo).then((response) => {
    return response.data;
  });
}

export async function getTodoInfoApi(todoHash: string) {
  return await axios
    .get(TODO_INFO, { params: { todo_hash: todoHash } })
    .then((response) => {
      return response.data;
    });
}

export async function getTodoApi(state: number) {
  return await axios
    .get(TODO, { params: { state: state } })
    .then((response) => {
      return response.data;
    });
}

export async function changeTodoStateApi(todoHash: string, stateRaw: number) {
  return axios
    .patch(TODO, { todo_hash: todoHash, state: stateRaw })
    .then((response) => response.data);
}

export async function addTodoNoteApi(todoHash: string, content: string) {
  return axios
    .post(TODO_NOTE, { todo_hash: todoHash, content: content })
    .then((response) => response.data);
}

export async function getNoteContentApi(todoHash: string, noteHash: string) {
  return axios
    .get(TODO_NOTE, { params: { todo_hash: todoHash, note_hash: noteHash } })
    .then((response) => response.data);
}

export async function getDateNotes() {
  return axios
    .get(DATE_NOTE, { params: { date: '' } })
    .then((response) => response.data);
}
