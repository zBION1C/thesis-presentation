<script setup>
defineProps({
  title: {
    type: String,
    default: "Definition",
  },
})
</script>

<template>
  <div class="definition-box">
    <div class="definition-title">{{ title }}</div>
    <div class="definition-content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.definition-box {
  background: #F8FAFC;
  border-radius: 3px;
}

.definition-title {
  font-weight: 600;
  color: #1D4ED8;
  padding-left: 0.35rem;
  margin-bottom: -1rem;
  letter-spacing: 0.02em;
}

.definition-content {
  color: #1F2933;
  line-height: 1.5;
  overflow-wrap: break-word;
  margin-left: 1rem;
}

.definition-content :deep(ul),
.definition-content :deep(ol) {
  padding-left: 2rem;
  margin: 0.5rem 0;
}

.definition-content :deep(li) {
  margin: 0.25rem 0;
}
</style>
