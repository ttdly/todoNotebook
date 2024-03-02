<template>
  <div class="item-content">
    <span class="todo-title" v-tooltip.top="todoInfo?.title">{{
      todoInfo?.title
    }}</span>
  </div>
  <slot name="notes"></slot>
  <div class="item-time">
    <i class="pi pi-calendar-plus"></i>
    <span>{{ todoInfo?.createDate }}</span>
    <template v-if="todoInfo?.state ==1">
      <span>-</span>
      <i class="pi pi-calendar-times"></i>
      <span>{{ todoInfo?.completeDate }}</span>
    </template>
  </div>
  <div class="item-botton" v-if="todoInfo.state == 0">
    <Button
      icon="pi pi-check"
      text
      rounded
      aria-label="Filter"
      v-tooltip.top="'完成'"
      @click="changeTodoState(1)"
    />
    <Button
      icon="pi pi-stop"
      text
      rounded
      aria-label="Filter"
      v-tooltip.top="'中止'"
      severity="danger"
      @click="changeTodoState(2)"
    />
    <slot name="default" v-if="todoInfo.state == 0"></slot>
  </div>
</template>

<script lang="ts" , setup>
import { type TodoObj, changeTodoStateApi } from '@/api';
import { type PropType } from 'vue';
const props = defineProps({
  todoInfo: {
    type: Object as PropType<TodoObj>,
    default: null,
  },
});

const emit = defineEmits(['refresh'])

const changeTodoState = async function (states: number) {
  console.log(states)
  const result = await changeTodoStateApi(props.todoInfo.hashCode, states);
  emit('refresh')
  return result;
};

</script>

<style scoped>
.todo-title {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  width: 20em;
  display: block;
}

.item-time {
  display: flex;
  gap: 4px;
  color: rgb(155, 155, 155);
  align-items: center;
}
</style>
