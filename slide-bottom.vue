<!-- global-bottom.vue -->
<template>
  <footer  
  v-if="$nav.currentLayout !== 'cover'"
  class="absolute bottom-0 left-0 right-0 pl-2 pr-2"
  style="color:grey;font-size:10px">
    <hr>
    <div class="flex items-center" style="justify-content: space-between">
      <span>
        Nicholas Montana, 1888414 - Department of Computer, Control and Management Engineering Antonio Ruberti
      </span>
      <img src="/public/images/logo.png" width=80 height=80>
    </div>
  </footer>
</template>
