<template>
  <div class="container">
    <div class="menu">
      <div>
        <template v-for="menuBar in menubarItems">
          <Button severity="secondary" :label="menuBar.label?.toString()" :icon="menuBar.icon?.toString()"
            @click="menuBar.command" text />
        </template>
      </div>
      <InputGroup v-if="addVisisble" class="add-todo">
        <InputGroupAddon>
          <Rating v-model="todoLevel" :cancel="false" :stars="3" v-tooltip.top="'一星随缘\n二星重要\n三星紧急'"/>
        </InputGroupAddon>
        <InputText placeholder="待办标题" v-model:model-value="todoTitle" />
        <Button icon="pi pi-check" severity="success" @click="addTodo()" />
      </InputGroup>
    </div>
    <div class="filter">
      <div class="level-filter">
        <div v-for="item in levelFilter" class="level-filter-item">
          <RadioButton v-model="levelSelected" :inputId="`levelcode${item.code}`" :value="item.code" @change="filterTodo(levelSelected, stateSelected)"/>
          <label :for="`levelcode${item.code}`">{{item.name}}</label>
        </div>
      </div>
      <div class="state-filter">
          <div class="state-filter-item" v-for="item in stateFilter">
            <RadioButton v-model="stateSelected" :inputId="`statecode${item.code}`" :value="item.code" @change="filterTodo(levelSelected, stateSelected)"/>
            <label :for="`statecode${item.code}`">{{item.name}}</label>
          </div>
        </div>
    </div>
    <div class="todos-container">
      <div v-for="item in visibleTodos" class="todo">
        <TodoItem :todo-info="item" @refresh="refreshTodoList">
          <Button icon="pi pi-plus" text rounded aria-label="Filter" v-tooltip.top="'记录'" severity="info"
            @click="showNoteDialog(item.hashCode)" />

          <template #notes>
            <Button icon="pi pi-book" text rounded aria-label="Filter" v-tooltip.top="'查看记录'" severity="info"
              @click="showNotes(item.hashCode)" />
          </template>
        </TodoItem>
      </div>
      <Dialog v-model:visible="visible" modal header="添加笔记" :style="{ width: '80ch' }">
        <div id="dialog-content">
          <Textarea rows="3" auto-resize v-model:model-value="noteContent" /><br />
          <div class="footer">
            <Button @click="createTodoNote">确认</Button>
          </div>
        </div>
      </Dialog>
      <Button class="close-window" v-if="contentVisible" @click="contentVisible = false" icon="pi pi-times"
        text></Button>
      <div class="notes-content" v-if="contentVisible">
        <ScrollPanel>
          <v-md-preview :text="markdownContent"></v-md-preview>
        </ScrollPanel>
      </div>
      <Button class="close-window" v-if="calendarVisible" @click="calendarVisible = false" icon="pi pi-times"></Button>

      <div class="notes-content calendar" v-if="calendarVisible">
        <div class="calendar-content">
          <MyCalendar :todo-event="todoEvents" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.level-filter, .state-filter{
  display: flex;
  gap: 12px;
}

.level-filter-item, .state-filter-item{
  display: flex;
  gap: 2px;
  align-items: center;
}

.filter {
  width: 100%;
  border: 1px solid #e2e8f0;
  color: #334155;
  border-radius: 5px;
  padding: 16px 10px;
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  margin-top: 10px;
}

.close-window {
  position: absolute;
  top: 1.4rem;
  right: 10.5rem;
  z-index: 9;
}

.p-scrollpanel {
  background: #fff;
  width: 100%;
  height: 100%;
}

.calendar-content {
  background: #fff;
  width: 930px;
  height: 720px;
  padding: 10px;
}

.notes-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  padding: 1rem 10rem;
}

.calendar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
}

.container {
  padding: 0.5rem 1rem;
  box-sizing: border-box;
}

.add-todo {
  margin-top: 5px;
}

.todos-container {
  display: flex;
  gap: 1rem;
  flex-direction: column;
  margin-top: 1rem;
}

.button-group {
  display: flex;
  justify-content: end;
  gap: 5px;
  margin-top: 5px;
}

.menu {
  border: 1px solid #e2e8f0;
  border-radius: 5px;
  padding: 10px;
}

.todo {
  width: 100%;
  border: 1px solid #e2e8f0;
  color: #334155;
  border-radius: 5px;
  padding: 5px 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.todo-title {
  text-overflow: ellipsis;
}

#dialog-content {
  display: flex;
  flex-direction: column;
}

.footer {
  display: flex;
  justify-content: end;
}
</style>

<script lang="ts" setup>
import type { MenuItem } from 'primevue/menuitem';
import { PrimeIcons } from 'primevue/api';
import { addTodoNoteApi, createTodoApi, getNoteContentApi, getTodoApi, type TodoObj } from '@/api';
import { ref, type Ref } from 'vue';
import TodoItem from '@/components/TodoItem.vue';
import MyCalendar from '@/components/MyCalendar.vue'

const test = ref();

const visible = ref(false);
const addVisisble = ref(false);
const contentVisible = ref(false);
const calendarVisible = ref(false);
const todoTitle = ref();
const todoLevel = ref(1)
const noteContent = ref();
const currTodoHash = ref();
const todos: Ref<Array<TodoObj>> = ref([]);
const visibleTodos: Ref<Array<TodoObj>> = ref([]);
const levelSelected = ref(1)
const stateSelected = ref(0)
const todoEvents = ref([])

const levelFilter = [
  { name: '全部', code: -1 },
  { name: '紧急', code: 0 },
  { name: '重要', code: 1 },
  { name: '随缘', code: 2 }
]
const stateFilter = [
  { name: '进行', code: 0 },
  { name: '中止', code: 2 },
  { name: '完成', code: 1 }
]
const markdownContent = ref("# www\n你好世界");
const menubarItems: MenuItem[] = [
  {
    label: '日历视图',
    icon: PrimeIcons.CALENDAR,
    command: () => {
      showCal();
    },
  },
  {
    label: '新建代办',
    icon: PrimeIcons.PENCIL,
    command: () => {
      addVisisble.value = !addVisisble.value;
    },
  },
];

const addTodo = async function () {
  if (todoLevel.value == 0) return;
  const todoObj: TodoObj = {
    title: todoTitle.value,
    state: 0,
    createDate: 'null',
    completeDate: 'null',
    level: handelLevelStar(),
    hashCode: ''
  };
  const result = await createTodoApi(todoObj);
  todoTitle.value = '';
  console.log(result);
  addVisisble.value = false;
  refreshTodoList();
};

function handelLevelStar():number{
  switch (todoLevel.value) {
    case 1:
      return 2;
    case 2:
      return 1;
    case 3:
      return 0;
    default:
      return 2;
  }
}


const refreshTodoList = async function () {
  const todoListRaw = await getTodoApi(stateSelected.value);
  todos.value = todoListRaw.msg;
  filterTodo(levelSelected.value, stateSelected.value)
};

const filterTodo = function (level: number, state: number) {
  visibleTodos.value = todos.value.filter(todo => {
    if (level == -1) return todo.state == state;
    return todo.level === level && todo.state === state
  })
}

const createTodoNote = async function () {
  const result = await addTodoNoteApi(currTodoHash.value, noteContent.value);
  visible.value = false;
  noteContent.value = '';
  currTodoHash.value = '';
  console.log(result);
};

const showNoteDialog = function (todoHash: string) {
  visible.value = true;
  currTodoHash.value = todoHash;
};

const showNotes = async function (todoHash: string) {
  console.log(todoHash)
  const result = await getNoteContentApi(todoHash, '')
  console.log(result);
  markdownContent.value = result.msg
  contentVisible.value = true
}

const showCal = async function () {
  calendarVisible.value = true
}


refreshTodoList();
</script>
