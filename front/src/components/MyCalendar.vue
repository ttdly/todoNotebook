<template>
  <FullCalendar :options="calendarOptions" />
</template>

<script lang="ts" setup>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import zhCnLocale from '@fullcalendar/core/locales/zh-cn'
import { type CalendarOptions } from '@fullcalendar/core';
const props = defineProps({
  todoEvent:{
    type:Array<EventSource>
  }
})
let url=''
if (import.meta.env.MODE === 'production') {
  // 生产环境逻辑
  url = '/api/date/note'
} else {
  url = 'http://127.0.0.1:5000/api/date/note'
}
const calendarOptions: CalendarOptions = {
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: zhCnLocale,
  height: '700px',
  events:{
    url: url
  }
}
// calendarOptions.events = props.todoEvent
</script>